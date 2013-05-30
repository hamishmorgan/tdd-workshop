

class Crawler:
    def __init__(self, urllib):
        self.urllib = urllib

    def crawl(self, initial_urls):
        self.urllib.urlopen('http://www.initialurl.com/')
        self.urllib.urlopen('http://testurl.com/testpage.html')

