import unittest

from crawler import AdjPhraseExtractor

class AdjPhraseExtractorTest(unittest.TestCase):
    def test_simple_extraction(self):
        html = """
<html><head><title="A nice web page"></head>
<body>
A big brown dog.
</body></html>
"""
        result = AdjPhraseExtractor.extract(html)
        self.assertEqual(result, [['big', 'brown', 'dog']])

