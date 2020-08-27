from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



class lookup():
    def __init__(self,query, results = 15):
        self.query = query
        self.results = results

    def search(self):
        url = f'https://duckduckgo.com/?q={self.query}'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        "result results_links_deep highlight_d result--url-above-snippet"
        '//*[@id="r1-1"]/div/h2/a[1]'

        links = {}
        linksContainer = driver.find_element_by_id('links')
        linksElements = linksContainer.find_elements_by_class_name('result__a')
        while len(linksElements) < self.results:
            moreButton = driver.find_element_by_css_selector('.result.result--more')
            moreButton.click()
            linksContainer = driver.find_element_by_id('links')
            linksElements = linksContainer.find_elements_by_class_name('result__a')
        for link in linksElements[0: self.results]:
            links[link.text] = link.get_attribute('href')
        return links


if __name__ == '__main__':
    x = input('Query: ')
    look = lookup(x, results= 100)
    links = look.search()
    print(links)


