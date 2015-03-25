import sqlite3

row_names = ('Newspaper', 'Heading', 'Detail', 'Date')

def escape_string(s):
    return s.replace('\'', '\'\'')

def query_all_headlines(location='headlines.db'):
    conn = sqlite3.connect(location)

    results = []

    with conn:
        cur = conn.cursor()
        cur.execute('select * from Headlines')
        
        rows = cur.fetchall()

        for row in rows:
            results.append(dict(zip(row_names, row)))

    return results

def query_custom(query, location='headlines.db'):
    conn = sqlite3.connect(location)

    results = []

    with conn:
        cur = conn.cursor()
        cur.execute(query)
        
        rows = cur.fetchall()

        for row in rows:
            results.append(dict(zip(row_names, row)))

    return results

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
