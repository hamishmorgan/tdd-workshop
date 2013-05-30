import unittest
import urllib2
from mock import create_autospec, call

from crawler.Crawler import Crawler

class CrawlerTest(unittest.TestCase):
    def test_crawler_recurses(self):
        # Arrange
        html = """
<html><body><a href="http://testurl.com/testpage.html">Link text</a></body></html>
"""
        initial_url = 'http://www.initialurl.com/'

        mock_urllib = create_autospec(urllib2)
        crawler = Crawler(mock_urllib)
        

        # Act
        crawler.crawl([initial_url])
        
        # Assert
        expected_calls = [call.urlopen(initial_url), call.urlopen('http://testurl.com/testpage.html')]
        mock_urllib.assert_has_calls(expected_calls)

        
