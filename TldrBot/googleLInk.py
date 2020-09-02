from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class lookup():
    def __init__(self,query, results = 15):
        self.query = query
        self.results = results
        self.setup()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def search(self):
        url = f'https://duckduckgo.com/?q={self.query}'

        self.driver.get(url)

        "result results_links_deep highlight_d result--url-above-snippet"
        '//*[@id="r1-1"]/div/h2/a[1]'

        links = {}
        linksContainer = self.driver.find_element_by_id('links')
        linksElements = linksContainer.find_elements_by_class_name('result__a')
        while len(linksElements) < self.results:
            moreButton = self.driver.find_element_by_css_selector('.result.result--more')
            moreButton.click()
            linksContainer = self.driver.find_element_by_id('links')
            linksElements = linksContainer.find_elements_by_class_name('result__a')
        for link in linksElements[0: self.results]:
            links[link.text] = link.get_attribute('href')
        return links
    def getAbstract(self):
        url = f'https://duckduckgo.com/?q={self.query}'
        self.driver.get(url)

        try:
            if self.driver.find_element_by_class_name('js-about-item-abstr'):
                x = self.driver.find_element_by_class_name('js-about-item-abstr')
                print(x.get_attribute('innerHTML'))
                return x.get_attribute('innerHTML')
            else:
                return None
        except:
            return None


class scrapeURLS():
    def __init__(self, urls, getElements = ['p', 'article','h1', 'h2', 'h3', 'h4', 'h5'], textOnly = True):
        self.urls = urls
        self.getElements = getElements
        self.textOnly = textOnly
        self.setup()
    def setup(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
    def scrape(self):
        returnObj = ''
        for url in self.urls:
            self.driver.get(url)
            for tag in self.getElements:
                for element in (self.driver.find_elements_by_tag_name(tag)):
                    returnObj += (element.get_attribute('innerHTML'))
        if self.textOnly:
            bs = BeautifulSoup(returnObj, 'html.parser')

            text = bs.text.replace('\n','')
            finalText = " ".join(text.split())
            return finalText

        return returnObj




if __name__ == '__main__':
    x = input('Query: ')
    look = lookup(x, results= 5)
    links = look.search()
    scrape = scrapeURL(links.values())
    print(scrape.scrape())



