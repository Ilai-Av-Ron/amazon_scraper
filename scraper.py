import concurrent.futures

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import database


def driver_init(country_code, ASIN=0, query=None):
    if country_code == 'us':
        url = 'https://www.amazon.com'
    elif country_code == 'de':
        url = 'https://www.amazon.de'
    elif country_code == 'uk':
        url = 'https://www.amazon.co.uk'
    elif country_code == 'ca':
        url = 'https://www.amazon.ca'
    if ASIN != 0:
        url = url + '/dp/' + ASIN
    else:
        url = url + '/s?k=' + query

    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def amazon_scraper(query, num_results=10):
    driver = driver_init('us', query=query)
    results = item_search(driver, query, int(num_results))
    get_results(query, driver, results)


def item_search(driver, query, num=10):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.select('div[data-asin]')[1:num + 1]
    items = []
    for result in results:
        ASIN = result['data-asin']
        items.append({
            'ASIN': ASIN,
            'result': result
        })
    return items


def get_results(query, driver, results):
    database.clear_qry_res()
    for i, result in enumerate(results):
        item = result['result']
        ASIN = result['ASIN']
        try:
            title = item.find('h2').text.strip()
            price_elem = item.find('span', {'class': 'a-price-whole'})
            if price_elem:
                price = price_elem.text.strip() + item.find('span', {'class': 'a-price-fraction'}).text.strip()
            else:
                price = 'N/A'
            rating = item.find('span', {'class': 'a-icon-alt'})
            if rating:
                rating = rating.text.strip()
                rating = float(rating.split()[0])
            else:
                rating = 'N/A'
            image_elem = item.find('img', {'class': 's-image'})
            if image_elem:
                image_url = image_elem['src']
            else:
                image_url = 'N/A'
            print('Result', i + 1)
            print('ASIN:', ASIN)
            print('Title:', title)
            print('Price:', price)
            print('Rating:', rating)
            print('-' * 50)
            database.update_qry_res(ASIN, query, title, rating, price, image_url)
        except Exception as e:
            print('Result', i + 1, 'failed:', e)
            print('-' * 50)


def convert_to_USD(price, country_code):
    conversion = {'ca': 0.73, 'uk': 1.25, 'de': 1.1}
    if country_code not in conversion:
        return price
    else:
        return round(price * conversion[country_code], 2)


def compare(query, email, ASIN):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(extract_price, 'uk', ASIN),
            executor.submit(extract_price, 'ca', ASIN),
            executor.submit(extract_price, 'de', ASIN)
        ]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    de_price, ca_price, uk_price = results
    print('uk', uk_price)
    print('ca', ca_price)
    print('de', de_price)
    title, price, image_url, rating = database.getData(ASIN)
    database.add_search(ASIN, query, title, price, ca_price, de_price, uk_price, image_url, email, rating)

def extract_price(country_code, ASIN):
    try:
        driver = driver_init(country_code, ASIN)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        price_elem = soup.find('span', {'class': 'a-price-whole'}) or soup.find('span', {'class': 'a-offscreen'})
        if price_elem:
            print(price_elem)
            price = price_elem.text.strip()
            if not price_elem.text.strip()[0].isdigit():
                price = price_elem.text.strip()[1:]
            else:
                price = price + soup.find('span', {'class': 'a-price-fraction'}).text.strip()
            price = price.replace(',', '.')
            price = convert_to_USD(float(price), country_code)
        else:
            price = 'N/A'
        print(f'{country_code} Price:', price)
    except:
        price = 'N/A'
        print(f'{country_code} Price:', price)
    finally:
        return price

