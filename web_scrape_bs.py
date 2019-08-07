import urllib3
from bs4 import BeautifulSoup

URL = 'https://www.indeed.com/jobs?q=Data+Scientist&l=Charlotte%2C+NC'

class IndeedScraper(object):
    '''
    get the long descriptions from Indeed.com job listings
    '''

    def __init__(self, url: str, pages: int):
        self.url = url
        self.http = urllib3.PoolManager()
        self.pages = pages

    def find_long_urls(self, soup):
        urls = []
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            for a in div.find_all(name='a', attrs={'class': 'jobtitle turnstileLink'}):
                urls.append(a['href'])
        return urls

    def get_next_pages(self):
        return [self.url] + [self.url + '&start=' + str(x) + '0' for x in range(1, self.pages)]

    def get_descriptions(self):
        descriptions = []
        for base_url in self.get_next_pages():
            request = self.http.request('GET', base_url)
            base_soup = BeautifulSoup(request.data)

            for url in self.find_long_urls(base_soup):
                the_url = 'http://www.indeed.com' + url
                req = self.http.request('GET', the_url,
                                        headers={'User-Agent': 'opera'},
                                        retries=urllib3.Retry(connect=500,
                                                              read=2, redirect=50))
                soup = BeautifulSoup(req.data, 'html.parser')
                description = soup.find(name='div', attrs={'id': 'jobDescriptionText'})
                descriptions.append(description.text)
        return descriptions

get_them = IndeedScraper(URL, 10).get_descriptions()
print(get_them)