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
    australian_words = process.get_all_australian_detail_words()
    herald_sun_words = process.get_all_herald_sun_detail_words()

    australian_cloud_words = process.to_cloud_words(australian_words, 25)
    herald_sun_cloud_words = process.to_cloud_words(herald_sun_words, 25)

    max_aus = max([x[1] for x in australian_cloud_words])
    min_aus = min([x[1] for x in australian_cloud_words])

    aus_domain = [min_aus, max_aus]

    max_hs = max([x[1] for x in herald_sun_cloud_words])
    min_hs = min([x[1] for x in herald_sun_cloud_words])

    hs_domain = [min_hs, max_hs]

    return render_template('cloud.html',
                            herald_sun_cloud_words=herald_sun_cloud_words,
                            australian_cloud_words=australian_cloud_words,
                            aus_domain=aus_domain,
                            hs_domain=hs_domain)

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
    app.debug = True
    app.run()
