import sqlite3
import os

def delete_duplicates(table, location='headlines.db'):
    """Delete duplicates

    Delete all duplicate headlines found in database.
    """

    conn = sqlite3.connect(location)

    with conn:
        cur = conn.cursor()
        query = 'delete from {} where rowid not in (select max(rowid) from {} group by Heading)';
        cur.execute(query.format(table))

def get_column_names_from_cursor(cursor):
    return [x[0] for x in cursor.description]

def query_get_banned_words():
    """Query get banned words

    Queries the database to find words that should not be included in the word cloud.

    Returns:
        A list of words.
    """
    
    rows = query_custom('select * from Banned_words')
    rows = [x[0] for x in rows]
    
    return rows

def escape_string(s):
    return s.replace('\'', '\'\'')

def query_all_headlines():
    """Query all headlines

    Queries the local database to look for all headlines.
    
    Returns:
        List of dictionary objects with headlines inside
    """
    
    results = query_custom_with_headers('select * from Headlines')

    return results

def query_custom_with_headers(query, location='headlines.db'):
    """Query custom 

    Send the database a custom sqlite3 query and get the rows returned.

    Args:
        Query to send to database
    
    Returns:
        List of rows selected.
    """
    conn = sqlite3.connect(location)

    with conn:
        cur = conn.cursor()
        cur.execute(query)
        
        rows = cur.fetchall()
        column_names = get_column_names_from_cursor(cur)

        results = []

        for row in rows:
            results.append(dict(zip(column_names, row)))

        return results

def query_custom(query, location='headlines.db'):
    """Query custom 

    Send the database a custom sqlite3 query and get the rows returned.

    Args:
        Query to send to database
    
    Returns:
        List of rows selected.
    """
    conn = sqlite3.connect(location)

    with conn:
        cur = conn.cursor()
        cur.execute(query)
        
        rows = cur.fetchall()
        return rows

def create_db(location):
    """Creates a database

    Creates a database with the proper setup for use with insertion of headlines.

    Args:
        Location of headline.
    """
    
    # Check if database already exists
    if os.path.isfile(location):
        print('Cannot create database, database already exists')
        return
    
    # Create database and put in default table
    open(location, 'w+').close()
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
