import sys
import requests
from bs4 import BeautifulSoup

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
        heading, detail = e.text.strip().split('\n')
        result.append({'heading': heading, 'detail': detail})

    return result

def main():

    print('-'*50)
    for headline in get_herald_sun_headlines():
        print('headline: {}\ndetail: {}'.format(headline['heading'], headline['detail']))
        print('-'*50)

if __name__ == '__main__':
    main()
