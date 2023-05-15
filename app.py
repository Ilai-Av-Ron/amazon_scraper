import sqlite3
from urllib.parse import urlencode

import requests
from flask import Flask, request, redirect
from google.auth.transport import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.auth.transport import requests
import google.auth.transport.requests
from requests import post
import google.auth.transport.requests
import requests

import database
import scraper

search_counts = {}

# maximum allowed searches per user per day
SEARCH_LIMIT = 10

app = Flask(__name__)
app.secret_key = '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'
app.config['SECRET'] = 'secret!'

conn = sqlite3.connect('database.db')
c = conn.cursor()

app = Flask(__name__)
app.secret_key = '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'


@app.route('/previous_searches')
def previous_searches():
    if 'google_token' in session:
        # Fetch user's email using access token
        headers = {'Authorization': 'Bearer ' + session['google_token']}
        response = requests.get('https://www.googleapis.com/userinfo/v2/me', headers=headers)
        email = response.json()['email']
        name = response.json()['name']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT item, rating, US_Price, UK_Price, CA_Price, DE_Price, image_url, datetime, query FROM searches WHERE email = ? ORDER BY datetime desc;', (email,))
        items = c.fetchall()
        conn.close()


        table_html = '<table style="border-collapse: collapse; width: 100%;"><thead><tr style="background-color: #f2f2f2;"><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Name</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Rating</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">US Price</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">UK Price</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">CA Price</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">DE Price</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Serach Date</th><th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Query</th><th style="padding: 8px; text-align: center;">Image</th></tr></thead><tbody>'
        for item in items:
            search_date = datetime.strptime(item[7], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            table_html += f'<tr><td style="width: 30%; text-align: center;">{item[0]}</td><td style="text-align: center;">{item[1]}</td><td style="text-align: center;">${item[2]}</td><td style="text-align: center;">${item[3]}</td><td style="text-align: center;">${item[4]}</td><td style="text-align: center;">${item[5]}</td><td style="text-align: center;">{search_date}</td><td style="text-align: center;">{item[8]}</td><td style="width: 30%; display: flex; justify-content: center; align-items: center; text-align: center; margin-left: 30px;"><img src="{item[6]}" alt="Image" style="max-width: 100%; max-height: 200px; display: block; margin: 0 auto;"></td></tr>'
        table_html += '</tbody></table>'

        return f'''
                <!DOCTYPE html>
                <html>
                <script>
                </script>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                            }}
                            th, td {{
                                text-align: left;
                                padding: 8px;
                                border-bottom: 1px solid #ddd;
                                margin-left: 30px;
                            }}
                            th {{
                                background-color: #4CAF50;
                                color: white;
                            }}
                            img {{
                                max-width: 100%;
                                max-height: 100%;
                            }}
                        </style>
                    </head>
                    <body>
                        <div style="display: flex; align-items: center; font-size: 1.2em; color: #333;">
                            <p style="margin-right: 10px;">Logged in as <strong>{name}</strong></p>
                            <form action="/search" method="get" style="display: flex; align-items: center;">
                                <input type="text" name="query" placeholder="Search..." style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <label for="num_results" style="margin-right: 10px;">Results:</label>
                                <input type="number" id="num_results" name="num_results" min="1" max="10" value="10" style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <button type="submit" style="background-color: #4CAF50; color: white; border: none; padding: 5px 15px; border-radius: 5px; height: 34px; cursor: pointer;" >Search</button>
                                <a href="/previous_searches" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Previous Searches</a>
                                <a href="/logout" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Logout</a>
                            </form>
                        </div>
                        <div>
                            {table_html}
                        </div>
                    </body>
                    <script>
                    </script>
                </html>
            '''
    else:
        # User is not logged in
        return f'''
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                                text-align: center;
                                margin-top: 50px;
                            }}
                            .header {{
                                font-size: 48px;
                                text-decoration: none;
                                color: #4CAF50;
                                font-weight: bold;
                            }}
                            a {{
                                display: inline-block;
                                padding: 15px 30px;
                                font-size: 24px;
                                font-weight: bold;
                                text-decoration: none;
                                color: #fff;
                                background-color: #4CAF50;
                                border-radius: 25px;
                                box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
                                transition: all 0.3s ease;
                            }}
                            a:hover {{
                                transform: translateY(-3px);
                                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
                            }}
                        </style>
                    </head>
                    <body>
                        <p><a href="/login">Login with Google</a> to use the Amazon scraper</p>
                    </body>
                </html>
            '''

@app.route('/compare_page')
def compare_page():
    if 'google_token' in session:
        # Fetch user's email using access token
        headers = {'Authorization': 'Bearer ' + session['google_token']}
        response = requests.get('https://www.googleapis.com/userinfo/v2/me', headers=headers)
        email = response.json()['email']
        name = response.json()['name']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT item, rating, US_Price, UK_Price, CA_Price, DE_Price, image_url, ASIN FROM searches WHERE email = ? ORDER BY datetime desc limit 1;', (email,))
        items = c.fetchall()
        conn.close()

        table_html = '<table><tr><th>Name</th><th>Rating</th><th>US Price</th><th>UK Price</th><th>CA Price</th><th>DE Price</th><th style="text-align:center;">Image</th></tr>'
        for item in items:
            us_link = f'<a href="https://www.amazon.com/dp/{item[7]}" target="_blank">${item[2]}</a>'
            uk_link = f'<a href="https://www.amazon.co.uk/dp/{item[7]}" target="_blank">${item[3]}</a>'
            ca_link = f'<a href="https://www.amazon.ca/dp/{item[7]}" target="_blank">${item[4]}</a>'
            de_link = f'<a href="https://www.amazon.de/dp/{item[7]}" target="_blank">${item[5]}</a>'
            table_html += f'<tr><td style="width: 38%">{item[0]}</td><td>{item[1]}</td><td>{us_link}</td><td>{uk_link}</td><td>{ca_link}</td><td>{de_link}</td><td style="width: 40%; display: flex; justify-content: center; align-items: center; text-align: center; margin-left: 28%;"><img src="{item[6]}" alt="Image" style="max-width: 100%; max-height: 100%; display: block;"></td></tr>'
        table_html += '</table>'

        return f'''
                <!DOCTYPE html>
                <html>
                <script>
                </script>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                            }}
                            th, td {{
                                text-align: left;
                                padding: 8px;
                                border-bottom: 1px solid #ddd;
                                margin-left: 30px;
                            }}
                            th {{
                                background-color: #4CAF50;
                                color: white;
                            }}
                            img {{
                                max-width: 100%;
                                max-height: 100%;
                            }}
                        </style>
                    </head>
                    <body>
                        <div style="display: flex; align-items: center; font-size: 1.2em; color: #333;">
                            <p style="margin-right: 10px;">Logged in as <strong>{name}</strong></p>
                            <form action="/search" method="get" style="display: flex; align-items: center;">
                                <input type="text" name="query" placeholder="Search..." style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <label for="num_results" style="margin-right: 10px;">Results:</label>
                                <input type="number" id="num_results" name="num_results" min="1" max="10" value="10" style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <button type="submit" style="background-color: #4CAF50; color: white; border: none; padding: 5px 15px; border-radius: 5px; height: 34px; cursor: pointer;" >Search</button>
                                <a href="/previous_searches" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Previous Searches</a>
                                <a href="/logout" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Logout</a>
                            </form>
                        </div>
                        <div>
                            {table_html}
                        </div>
                    </body>
                    <script>
                    </script>
                </html>
            '''
    else:
        # User is not logged in
        return f'''
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                                text-align: center;
                                margin-top: 50px;
                            }}
                            .header {{
                                font-size: 48px;
                                text-decoration: none;
                                color: #4CAF50;
                                font-weight: bold;
                            }}
                            a {{
                                display: inline-block;
                                padding: 15px 30px;
                                font-size: 24px;
                                font-weight: bold;
                                text-decoration: none;
                                color: #fff;
                                background-color: #4CAF50;
                                border-radius: 25px;
                                box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
                                transition: all 0.3s ease;
                            }}
                            a:hover {{
                                transform: translateY(-3px);
                                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
                            }}
                        </style>
                    </head>
                    <body>
                        <p><a href="/login">Login with Google</a> to use the Amazon scraper</p>
                    </body>
                </html>
            '''


@app.route('/compare')
def compare():
    ASIN = request.args.get('query')
    if 'google_token' in session:
        # Fetch user's email using access token
        headers = {'Authorization': 'Bearer ' + session['google_token']}
        response = requests.get('https://www.googleapis.com/userinfo/v2/me', headers=headers)
        email = response.json()['email']
        query = database.get_query(ASIN)
        scraper.compare(query, email, ASIN)
        return redirect('/compare_page')
    else:
        # User is not logged in
        return f'''
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                                text-align: center;
                                margin-top: 50px;
                            }}
                            .header {{
                                font-size: 48px;
                                text-decoration: none;
                                color: #4CAF50;
                                font-weight: bold;
                            }}
                            a {{
                                display: inline-block;
                                padding: 15px 30px;
                                font-size: 24px;
                                font-weight: bold;
                                text-decoration: none;
                                color: #fff;
                                background-color: #4CAF50;
                                border-radius: 25px;
                                box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
                                transition: all 0.3s ease;
                            }}
                            a:hover {{
                                transform: translateY(-3px);
                                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
                            }}
                        </style>
                    </head>
                    <body>
                        <p><a href="/login">Login with Google</a> to use the Amazon scraper</p>
                    </body>
                </html>
            '''



@app.route('/')
def index():
    if 'google_token' in session:
        # Fetch user's email using access token
        headers = {'Authorization': 'Bearer ' + session['google_token']}
        response = requests.get('https://www.googleapis.com/userinfo/v2/me', headers=headers)
        email = response.json()['email']
        name = response.json()['name']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT item, rating, US_Price, image_url, ASIN FROM query_results')
        items = c.fetchall()
        conn.close()

        table_html = '<table><tr><th>Name</th><th>Rating</th><th>US Price</th><th style="text-align:center;">Image</th></tr>'
        for item in items:
            table_html += f'<tr><td style="width: 38%"><a>{item[0]}</a><form action="/compare" method="get" style="margin-left: 10px; display: flex; align-items: center;"><input type="hidden" name="query" value="{item[4]}"><button type="submit" style="background-color: #4CAF50; color: white; border: none; padding: 5px 15px; border-radius: 5px; height: 34px; cursor: pointer;" >Compare to regional prices</button></form></td><td>{item[1]}</td><td><a >${item[2]}</a></td><td style="width: 40%; display: flex; justify-content: center; align-items: center; text-align: center; margin-left: 28%;"><img src="{item[3]}" alt="Image" style="max-width: 100%; max-height: 100%; display: block;"></td></tr>'
        table_html += '</table>'

        return f'''
                <!DOCTYPE html>
                <html>
                <script>
                </script>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                            }}
                            th, td {{
                                text-align: left;
                                padding: 8px;
                                border-bottom: 1px solid #ddd;
                                margin-left: 30px;
                            }}
                            th {{
                                background-color: #4CAF50;
                                color: white;
                            }}
                            img {{
                                max-width: 100%;
                                max-height: 100%;
                            }}
                        </style>
                    </head>
                    <body>
                        <div style="display: flex; align-items: center; font-size: 1.2em; color: #333;">
                            <p style="margin-right: 10px;">Logged in as <strong>{name}</strong></p>
                            <form action="/search" method="get" style="display: flex; align-items: center;">
                                <input type="text" name="query" placeholder="Search..." style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <label for="num_results" style="margin-right: 10px;">Results:</label>
                                <input type="number" id="num_results" name="num_results" min="1" max="10" value="10" style="margin-right: 10px; border: 1px solid #ccc; padding: 5px; border-radius: 5px;">
                                <button type="submit" style="background-color: #4CAF50; color: white; border: none; padding: 5px 15px; border-radius: 5px; height: 34px; cursor: pointer;" >Search</button>
                                <a href="/previous_searches" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Previous Searches</a>
                                <a href="/logout" style="margin-left: 10px; color: white; text-decoration: none; background-color: #4CAF50; border: none; padding: 5px 15px; border-radius: 5px; height: 34px;">Logout</a>
                            </form>
                        </div>
                        <div>
                            {table_html}
                        </div>
                    </body>
                    <script>
                    </script>
                </html>
            '''
    else:
        # User is not logged in
        return f'''
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Amazon Scraper</title>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                        <style>
                            body {{
                                font-family: 'Open Sans', sans-serif;
                                text-align: center;
                                margin-top: 50px;
                            }}
                            .header {{
                                font-size: 48px;
                                text-decoration: none;
                                color: #4CAF50;
                                font-weight: bold;
                            }}
                            a {{
                                display: inline-block;
                                padding: 15px 30px;
                                font-size: 24px;
                                font-weight: bold;
                                text-decoration: none;
                                color: #fff;
                                background-color: #4CAF50;
                                border-radius: 25px;
                                box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
                                transition: all 0.3s ease;
                            }}
                            a:hover {{
                                transform: translateY(-3px);
                                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
                            }}
                        </style>
                    </head>
                    <body>
                        <p><a href="/login">Login with Google</a> to use the Amazon scraper</p>
                    </body>
                </html>
            '''


from datetime import datetime
from flask import session


@app.route('/search')
def search():
    # get the user's email
    headers = {'Authorization': 'Bearer ' + session['google_token']}
    response = requests.get('https://www.googleapis.com/userinfo/v2/me', headers=headers)
    user_email = response.json()['email']
    name = response.json()['name']

    # check if the user has exceeded the daily search limit
    if user_email in search_counts and search_counts[user_email]['date'] == datetime.now().date():
        if search_counts[user_email]['count'] >= SEARCH_LIMIT:
            return redirect('/max_searches?username=' + name)

    # increment the user's daily search count
    if user_email not in search_counts or search_counts[user_email]['date'] != datetime.now().date():
        search_counts[user_email] = {'count': 1, 'date': datetime.now().date()}
    else:
        search_counts[user_email]['count'] += 1

    query = request.args.get('query')
    num_results = request.args.get('num_results')
    scraper.amazon_scraper(query, num_results)
    return redirect('/')

@app.route('/max_searches')
def max_searches():
    username = request.args.get('username')
    return f'''
                <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Daily Search Cap Reached</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">Amazon</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Today's Deals <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Customer Service</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Gift Cards</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Registry</a>
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container my-5">
        <div class="row">
            <div class="col-md-4">
            </div>
            <div class="col-md-8">
                <h1 class="mb-3">Sorry, {username}, daily search cap reached 😞</h1>
                <p class="lead mb-5">Consider upgrading to the premium service in order to search for more items.</p>
                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s" class="btn btn-lg btn-warning mr-3">Upgrade to Premium</a>
                <a href="/logout" class="btn btn-lg btn-outline-secondary">Back to Home</a>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-light text-center py-3">
        <div class="container">
            <span class="text-muted">Copyright &copy; 2023
                <a href="www.Amazon.com">Amazon.com</a>. All rights reserved.
            </span>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"
        integrity="sha384-vfFKbHwr+tO5Z0bXg5l5j5H5iBpwhKPKW8VODlo6ncrossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
    integrity="sha384-LzApL6Cw5RpLAeDl6v3Z3aHksXuug8LW+M6vFE3V4N4E4JNQ5kkA4TCfCIF+ZJXn"
    crossorigin="anonymous"></script>
    </body>
</html>
            '''


@app.route("/login")
def login():
    auth_url = 'https://accounts.google.com/o/oauth2/auth'
    params = {
        'client_id': '965754551330-f8v11k1tqf2q45320ta7pmmiolvu84n4.apps.googleusercontent.com',
        'redirect_uri': 'http://localhost:5000/login/callback',
        'scope': 'email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    url = auth_url + '?' + urlencode(params)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM query_results')
    conn.commit()
    return redirect(url)

@app.route('/login/callback')
def login_callback():
    # Get the authorization code from the callback URL
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token = post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': '965754551330-f8v11k1tqf2q45320ta7pmmiolvu84n4.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': 'http://localhost:5000/login/callback',
        'grant_type': 'authorization_code',
    }).json()

    # Verify the ID token
    idinfo = id_token.verify_oauth2_token(token['id_token'], Request())

    # Store the access token in the session
    session['google_token'] = token['access_token']

    # Redirect to the main page
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)