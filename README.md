A pretty basic amazon product scraper, comprised of three main python files:

1. app.py (The flask app used for the site)
2. scraper.py (The code responsible for the scraping functionality)
3. database.py (Managing the databases holding the search results)

There's also the actual database. Might need a json for google authentication.

You can run the main app by using the 'flask run' command from the terminal, and accessing the server (http://localhost:5000/).
You must log-in (via google) in order to use the scraper, you can search for a product, and compare it's prices with different Amazon regions. Can also view your search history.

Enjoy!
