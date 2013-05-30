# Extract adjective phrases from html

from bs4 import BeautifulSoup
import nltk


def extract(html, tagger=nltk.pos_tag, tokenizer=nltk.word_tokenize):
    # boundary condition check
    if not html:
        return None

    soup = BeautifulSoup(html)

    # boundary condition check
    text = soup.body.text.strip()
    if not text:
        return []

    tokens = tokenizer(text)
    tagged_text = tagger(tokens)
    sequences = list()

    try:
        it = iter(tagged_text)
        word, tag = next(it)
        while True:
            while tag != 'JJ':
                word, tag = next(it)
            sequence = list()
            while tag == 'JJ':
                sequence.append(word)
                word, tag = next(it)
            if tag == 'NN':
                try:
                    while tag == 'NN':
                        sequence.append(word)
                        word, tag = next(it)
                finally:
                    sequences.append(sequence)
    except StopIteration:
        pass
    return sequences

