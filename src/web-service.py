from flask import Flask, jsonify, render_template
import itertools
import scrape
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/cloud', methods=['GET'])
def words():
    words = []

    headlines = get_current_headlines();

    details = [h['detail'] for h in headlines['headlines']]
    details = [h.lower().split() for h in details]
    details = list(itertools.chain(*details)) 

    return render_template('cloud.html', words=details)

@app.route('/scrape/api/v1.0/latest', methods=['GET'])
def latest():
    result = get_latest_headlines()
    return jsonify(result)

@app.route('/scrape/api/v1.0/current', methods=['GET'])
def current():
    result = get_current_headlines()
    return jsonify(result)

def get_latest_headlines():
    # Go get the top 5 latest from each newspaper
    aus = scrape.get_australian_headlines()[:5]
    hs = scrape.get_herald_sun_headlines()[:5]
    
    result = {'headlines': aus+hs}

    return result 

def get_current_headlines():
    # Go get the latest from each newspaper
    aus = scrape.get_australian_headlines()
    hs = scrape.get_herald_sun_headlines()
    
    result = {'headlines': aus+hs}

    return result

if __name__ == '__main__':
    app.run(debug=True)
