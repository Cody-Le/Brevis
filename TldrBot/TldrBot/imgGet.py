import requests
from bs4 import BeautifulSoup as bs
import re



class imgGetter():
    def __init__(self, query):
        self.query = query
        print(self.query)
    def getImg(self):
        returnLinks = []

        url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(self.query)
        print(url)
        html = requests.get(url).text
        soup = bs(html, 'html.parser')

        for link in soup.find_all('img'):
            x = link.get('src')
            print(x)
            r = re.compile('http.*//.*')
            if r.match(x) is not None:
                returnLinks.append(x)
                print('confirm', x)
                return x

if __name__ == '__main__':
    x= input('Enter a query: ')
    getter = imgGetter(query = x)
    print(getter.getImg())
