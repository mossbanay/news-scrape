# news-scrape

News-scrape is a project to help illustrate what Australian newspapers choose to discuss by use of word cloud. The service fetches and stores headlines in a sqlite3 database and fetches them when need be. Flask is used as the web server while requests and BeautifulSoup are used for fetching and parsing the headlines from the tabloid websites.

# Usage

To run the project locally, do: `python web-service.py` from the src directory.

Running `python update-database.py` will go and fetch new headlines. It is recommended to run this via cron to save the hassle of running the script every now and then while still maintaining an up to date database.

# Screenshot

Below is a screenshot of the project in the wake of two major news events, the election of Mike Baird as NSW Premier and the murder of Masa Vukotic.
![](https://raw.githubusercontent.com/leaen/news-scrape/master/screenshot.png)

# Credits

This project uses d3-cloud wrriten by Jason Davies (jasondavies)
