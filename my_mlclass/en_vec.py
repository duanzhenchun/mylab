from Stemmer import Stemmer
import re
import numpy as np


stem = Stemmer('en').stemWord

def load_voc(fname):
    with open(fname) as fo:
        kv = (line.split() for line in fo)
        return dict((v.strip(), int(k)) for k, v in kv)


def normailze(text):
    text = text.lower()
    text = re.sub('<[^<>]+>', ' ', text)
    text = re.sub('[0-9]+', 'number', text)
    text = re.sub('(http|https)://[^\s]*', 'httpaddr', text)
    text = re.sub('[^\s]+@[^\s]+', 'emailaddr', text)
    text = re.sub('\$+', 'dollar', text)
    return text


def tokenize(text):
    text = normailze(text)
    tokens = re.split(r'[ @$/#.\-:&*+=\[\]?!(){},\'">_<;%\n\r]', text)
    tokens = (re.sub('[^a-zA-Z]', '', token) for token in tokens)
    return (stem(token) for token in tokens if token.strip())


def vectorize(voc, text):
    vec = np.zeros(len(voc))
    for token in tokenize(text):
        i = voc.get(token, -1)
        if i == -1:
            continue
        vec[i] = 1
    return vec
