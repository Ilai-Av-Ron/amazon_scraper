import datetime
import sqlite3

# connect to the database
conn = sqlite3.connect('database.db')

# create a table
conn.execute('''CREATE TABLE IF NOT EXISTS query_results
             (ASIN text PRIMARY KEY, query TEXT, item TEXT, rating REAL, US_Price REAL, image_url TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS searches
             (ASIN text PRIMARY KEY, query TEXT, datetime DATETIME, item TEXT, US_Price REAL, CA_Price REAL, DE_Price REAL, UK_Price REAL, image_url TEXT, email TEXT, rating FLOAT)''')

def clear_qry_res():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM query_results")
    conn.commit()


def get_query(ASIN):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''SELECT query
                       FROM query_results
                       WHERE ASIN = ?
                       LIMIT 1''', (ASIN,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    else:
        query = row[0]
        return query


def update_qry_res(ASIN, query, item, rating, price, image_url):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''Insert into query_results (ASIN, query, item, rating, US_Price, image_url) VALUES (?, ?, ?, ?, ?, ?)''',
    (ASIN, query, item, rating, price, image_url))
    conn.commit()



def add_search(ASIN, query, item, US_Price, CA_Price, DE_Price, UK_Price, image_url, email, rating):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    now = datetime.datetime.now()
    cur.execute("""INSERT OR REPLACE INTO searches (ASIN, query, datetime, item, US_Price, CA_Price, DE_Price, UK_Price, image_url, email, rating)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (ASIN, query, now, item, US_Price, CA_Price, DE_Price, UK_Price, image_url, email, rating))
    conn.commit()
    conn.close()


def getData(ASIN):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''SELECT item, US_Price, image_url, rating
                   FROM query_results
                   WHERE ASIN = ?
                   LIMIT 1''', (ASIN,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    else:
        item, us_price, image_url, rating = row
        return (item, us_price, image_url, rating)


# commit the changes
conn.commit()

# close the connection
conn.close()