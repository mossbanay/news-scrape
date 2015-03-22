import scrape
import os

# Check if db exists
if os.path.isfile('headlines.db') == False:
    scrape.create_db('headlines.db')

# Update db
aus = scrape.get_australian_headlines()
hs = scrape.get_herald_sun_headlines()

scrape.save_to_db('headlines.db', aus)
scrape.save_to_db('headlines.db', hs)
