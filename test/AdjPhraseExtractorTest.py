import unittest

from mock import Mock

from crawler import AdjPhraseExtractor


class AdjPhraseExtractorTest(unittest.TestCase):
    def test_simple_extraction(self):
        html = """
<html><head><title="A nice web page"></head>
<body>
A big brown dog.
</body></html>
"""
        mocked_tokenizer = Mock(return_value=['A', 'big', 'brown', 'dog', '.'])
        mocked_tagger = Mock(return_value=[(u'A', 'DT'), (u'big', 'JJ'), (u'brown', 'JJ'), (u'dog', 'NN'), (u'.', '.')])

        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertEqual(result, [['big', 'brown', 'dog']])

    def test_empty_extraction(self):
        html = """<html><head><title="empty"></head>
<body>
</body></html>"""
        mocked_tokenizer = Mock(return_value=[])
        mocked_tagger = Mock(return_value=[])

        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertEqual(result, [])

    #
    def test_null_extraction(self):
        html = None
        mocked_tokenizer = Mock(return_value=[])
        mocked_tagger = Mock(return_value=[])
        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertIsNone(result)

    def test_ignore_cdata(self):
        html = """<html><head><title="Brighton"></head>
<body><![CDATA[ A small yellow cat. ]]>  A big brown dog.
</body></html>"""
        mocked_tokenizer = Mock(return_value=['A', 'big', 'brown', 'dog', '.'])
        mocked_tagger = Mock(return_value=[(u'A', 'DT'), (u'big', 'JJ'), (u'brown', 'JJ'), (u'dog', 'NN'), (u'.', '.')])
        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertEqual(result, [['big', 'brown', 'dog']])

    def test_invalid_html_extraction(self):
        html = """<html><head><title="Brighton"></head>
<body></what></the><hell>"""
        mocked_tokenizer = Mock(return_value=[])
        mocked_tagger = Mock(return_value=[])
        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertEqual(result, [])

    def test_ignore_comments(self):
        html = """<html><head><title="Brighton"></head>
<body><!-- A small yellow cat. -->  A big brown dog.
</body></html>"""
        mocked_tokenizer = Mock(return_value=['A', 'big', 'brown', 'dog', '.'])
        mocked_tagger = Mock(return_value=[(u'A', 'DT'), (u'big', 'JJ'), (u'brown', 'JJ'), (u'dog', 'NN'), (u'.', '.')])
        result = AdjPhraseExtractor.extract(html, tokenizer=mocked_tokenizer, tagger=mocked_tagger)
        self.assertEqual(result, [['big', 'brown', 'dog']])

    def test_not_brown_extraction(self):
        html = """
<html><head><title="A nice web page"></head>
<body>
A big yellow dog.
</body></html>
"""
        mocked_tokenizer = Mock(return_value=['A', 'big', 'yellow', 'dog', '.'])
        mocked_tagger = Mock(
            return_value=[(u'A', 'DT'), (u'big', 'JJ'), (u'yellow', 'JJ'), (u'dog', 'NN'), (u'.', '.')])
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)

        mocked_tokenizer.assert_called_once_with('A big yellow dog.')
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [['big', 'yellow', 'dog']])

    def test_two_words(self):
        html = """<html><head><title="Brighton"></head><body>red dog</body></html>"""
        mocked_tokenizer = Mock(return_value=['red', 'dog'])
        mocked_tagger = Mock(return_value=[(u'red', 'JJ'), (u'dog', 'NN')])
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)

        mocked_tokenizer.assert_called_once_with('red dog')
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [['red', 'dog']])


    def test_ignore_html(self):
        html = """<html><head><title="Brighton"></head><body><red tree />green boat</body></html>"""
        mocked_tokenizer = Mock(return_value=['green', 'boat'])
        mocked_tagger = Mock(return_value=[(u'green', 'JJ'), (u'boat', 'NN')])
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)

        mocked_tokenizer.assert_called_once_with('green boat')
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [['green', 'boat']])


    def test_no_nouns_extraction(self):
        html = """<html><head><title="empty"></head>
<body>red green blue
</body></html>"""
        mocked_tokenizer = Mock(return_value=['red', 'green', 'blue'])
        mocked_tagger = Mock(return_value=[(u'red', 'JJ'), (u'green', 'JJ'), (u'blue', 'JJ')])
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)
        mocked_tokenizer.assert_called_once_with('red green blue')
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [])

    #
    def test_no_adj_extraction(self):
        html = """<html><head><title="empty"></head>
<body>tree rock plan explosion
</body></html>"""
        mocked_tokenizer = Mock(return_value=['tree', 'rock', 'plant', 'explosion'])
        mocked_tagger = Mock(return_value=[(u'tree', 'NN'), (u'rock', 'NN'), (u'plant', 'NN'), (u'explosion', 'NN')])
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)
        mocked_tokenizer.assert_called_once_with('tree rock plan explosion')
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [])

    #

    def test_longer_extraction(self):
        text = """The ancient settlement of Brighthelmstone dates from before Domesday Book (1086), but it emerged as a health resort
featuring sea bathing during the 18th century and became a destination for day-trippers from London after the arrival
of the railway in 1841. Brighton experienced rapid population growth, reaching a peak of over 160,000 by 1961.
Modern Brighton forms part of the Brighton/Worthing/Littlehampton conurbation stretching along the coast, with a
population of around 480,000 inhabitants."""

        tokens = ['The', 'ancient', 'settlement', 'of', 'Brighthelmstone', 'dates', 'from', 'before', 'Domesday',
                  'Book', '(', '1086', ')', ',', 'but', 'it', 'emerged', 'as', 'a', 'health', 'resort', 'featuring',
                  'sea', 'bathing', 'during', 'the', '18th', 'century', 'and', 'became', 'a', 'destination', 'for',
                  'day-trippers', 'from', 'London', 'after', 'the', 'arrival', 'of', 'the', 'railway', 'in', '1841.',
                  'Brighton', 'experienced', 'rapid', 'population', 'growth', ',', 'reaching', 'a', 'peak', 'of',
                  'over', '160,000', 'by', '1961', '.', 'Modern', 'Brighton', 'forms', 'part', 'of', 'the',
                  'Brighton/Worthing/Littlehampton', 'conurbation', 'stretching', 'along', 'the', 'coast', ',', 'with',
                  'a', 'population', 'of', 'around', '480,000', 'inhabitants', '.']

        tags = [('The', 'DT'), ('ancient', 'JJ'), ('settlement', 'NN'), ('of', 'IN'), ('Brighthelmstone', 'NNP'),
                ('dates', 'VBZ'), ('from', 'IN'), ('before', 'IN'), ('Domesday', 'NNP'), ('Book', 'NNP'), ('(', 'NNP'),
                ('1086', 'CD'), (')', 'CD'), (',', ','), ('but', 'CC'), ('it', 'PRP'), ('emerged', 'VBD'), ('as', 'IN'),
                ('a', 'DT'), ('health', 'NN'), ('resort', 'NN'), ('featuring', 'VBG'), ('sea', 'NN'),
                ('bathing', 'VBG'),
                ('during', 'IN'), ('the', 'DT'), ('18th', 'JJ'), ('century', 'NN'), ('and', 'CC'), ('became', 'VBD'),
                ('a', 'DT'), ('destination', 'NN'), ('for', 'IN'), ('day-trippers', 'NNS'), ('from', 'IN'),
                ('London', 'NNP'), ('after', 'IN'), ('the', 'DT'), ('arrival', 'NN'), ('of', 'IN'), ('the', 'DT'),
                ('railway', 'NN'), ('in', 'IN'), ('1841.', 'CD'), ('Brighton', 'NNP'), ('experienced', 'VBD'),
                ('rapid', 'JJ'), ('population', 'NN'), ('growth', 'NN'), (',', ','), ('reaching', 'VBG'), ('a', 'DT'),
                ('peak', 'NN'), ('of', 'IN'), ('over', 'IN'), ('160,000', 'CD'), ('by', 'IN'), ('1961', 'CD'),
                ('.', '.'), ('Modern', 'NNP'), ('Brighton', 'NNP'), ('forms', 'NNS'), ('part', 'NN'), ('of', 'IN'),
                ('the', 'DT'), ('Brighton/Worthing/Littlehampton', 'NNP'), ('conurbation', 'NN'), ('stretching', 'VBG'),
                ('along', 'IN'), ('the', 'DT'), ('coast', 'NN'), (',', ','), ('with', 'IN'), ('a', 'DT'),
                ('population', 'NN'), ('of', 'IN'), ('around', 'IN'), ('480,000', 'CD'), ('inhabitants', 'NNS'),
                ('.', '.')]

        html = """<html><head><title="Brighton"></head><body>""" + text + """</body></html>"""
        mocked_tokenizer = Mock(return_value=tokens)
        mocked_tagger = Mock(return_value=tags)
        result = AdjPhraseExtractor.extract(html, tagger=mocked_tagger, tokenizer=mocked_tokenizer)
        mocked_tokenizer.assert_called_once_with(text)
        mocked_tagger.assert_called_once_with(mocked_tokenizer.return_value)
        self.assertEqual(result, [['ancient', 'settlement'], ['18th', 'century'], ['rapid', 'population', 'growth']])

