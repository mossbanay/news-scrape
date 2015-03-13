import sys
import requests
from bs4 import BeautifulSoup

def main():
    news_url = 'http://www.heraldsun.com.au/news/top-stories'
    resp = requests.get(news_url)
    soup = BeautifulSoup(resp.content)

    content_section = soup.findAll('div', attrs={'id':'content-2'})[0]
    headlines = content_section.findAll('h4', attrs={'class':'heading'})

    for headline in headlines:
        print(headline.text)

if __name__ == '__main__':
    main()
