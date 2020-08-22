import requests
from bs4 import BeautifulSoup as bs
import re



class imgGet():
    def __init__(self, query):
        self.query = query
        print(self.query)
    def getImg(self):
        returnLinks = []

        url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(self.query)

        html = requests.get(url).text
        soup = bs(html, 'html.parser')

        for link in soup.find_all('img'):
            x = link.get('src')
            r = re.compile('http.*//.*')
            if r.match(x) is not None:
                returnLinks.append(x)
                return x

if __name__ == '__main__':
    x= input('Enter a query: ')
    getter = imgGet(query = x)
    print(getter.getImg())
