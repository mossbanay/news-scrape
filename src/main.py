import sys
import requests
import sqlite3
import os
from bs4 import BeautifulSoup

def escape_string(s):
    return s.replace('\'', '\'\'')

def create_db(location):
    """Creates a database

    Creates a database with the proper setup for use with insertion of headlines.

    Args:
        Location of headline.
    """
    
    # Check if database already exists
    if os.path.isfile(location) == True:
        print('Cannot create database, database already exists')
        return
    
    # Create database and put in default table
    db = open(location, 'w+').close()
    conn = sqlite3.connect(location)

    with conn:
        cur = conn.cursor()
        
        cur.execute("CREATE TABLE Headlines(Newspaper TEXT, Heading TEXT, Detail TEXT, Date DATETIME)")

def save_to_db(location, headlines):
    """Save headlines to database
    
    Connects to the local database and inserts an array of headline dictionaries.

    Args:
        Location of database to open.
        Array of headlines.
    
    Raises:
        sqlite3.Error: An error occured when communicating with the database.
    """
   
    # Get a connection to the database
    conn = sqlite3.connect(location) 

    with conn:
        cur = conn.cursor()
        
        for headline in headlines:
            # (Newspaper, Heading, Detail, Date) 
            command = "INSERT INTO Headlines VALUES ('{}', '{}', '{}', DATETIME('now'));"
            command = command.format(escape_string(headline['newspaper']),
                                     escape_string(headline['heading']),
                                     escape_string(headline['detail']))

            cur.execute(command)

def get_australian_headlines():
    """Gets The Australian headlines.

    Makes a request to The Australian's website and retrieves the headlines from the
    latest news page.

    Returns:
        A list of dictionary objects containing a heading and detail for each headline.
    """
    news_url = 'http://www.theaustralian.com.au/news/latest-news'
    resp = requests.get(news_url)
    soup = BeautifulSoup(resp.content)

    content_section = soup.findAll('div', attrs={'id':'content-2'})[0].findAll('div', attrs={'class':'module-content'})[0]
    headlines = content_section.findAll('div', attrs={'class':'story-block'})

    result = []
    for e in headlines:
        heading, _, detail = e.text.strip().split('\n')
        
        # Remove 'read more'
        detail = detail[:-10]

        result.append({'newspaper': 'the-australian', 'heading': heading, 'detail': detail})

    return result

def get_herald_sun_headlines():
    """Gets Herald Sun headlines.

    Makes a request to the Herald Sun website and retrieves the headlines from the
    top stories page.

    Returns:
        A list of dictionary objects containing a heading and detail for each headline.
    """
    news_url = 'http://www.heraldsun.com.au/news/top-stories'
    resp = requests.get(news_url)
    soup = BeautifulSoup(resp.content)

    content_section = soup.findAll('div', attrs={'id':'content-2'})[0]
    headlines = content_section.findAll('h4', attrs={'class':'heading'})
    
    result = []
    for e in headlines:
        headline = e.text.strip()
        if '\n' in headline:
            heading, detail = headline.split('\n')
        else:
            heading, detail = headline, headline

        result.append({'newspaper': 'herald-sun', 'heading': heading, 'detail': detail})

    return result
