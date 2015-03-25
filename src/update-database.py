import scrape
import database
import os

# Check if db exists
if os.path.isfile('headlines.db') == False:
    database.create_db('headlines.db')

# Update db
aus = scrape.get_australian_headlines()
hs = scrape.get_herald_sun_headlines()

database.save_to_db('headlines.db', aus)
database.save_to_db('headlines.db', hs)
