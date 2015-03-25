from flask import Flask, jsonify, render_template
import itertools
import scrape
import process

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/cloud', methods=['GET'])
def words():
    cloud_words = process.get_all_detail_cloud_words(50)

    return render_template('cloud.html', cloud_words=cloud_words)

@app.route('/scrape/api/v1.0/latest', methods=['GET'])
def latest():
    result = get_latest_headlines()
    return jsonify(result)

def get_latest_headlines():
    # Go get the top 5 latest from each newspaper
    aus = scrape.get_australian_headlines()[:5]
    hs = scrape.get_herald_sun_headlines()[:5]
    
    result = {'headlines': aus+hs}

    return result 

if __name__ == '__main__':
    app.run(debug=True)
