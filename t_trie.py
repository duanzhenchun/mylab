_v = 0


# https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python
class Trie():
    def __init__(self):
        self.root = {}  # use embeded diction, not links

    def insert(self, word, v):
        p = self.root
        for c in word:
            p = p.setdefault(c, {})  # trick to get existed children
        p[_v] = v   # set leaf value

    def remove(self, word):
        p = self._lookup(word)
        if not p:
            print '%s not in trie' %word
        else:
            del p[_v]       # empty {} may remains for parent

    def _lookup(self, word):
        p = self.root
        for c in word:
            if c not in p:
                return None
            p = p[c]
        return p

    def _travel(self, p):
        for c in p:
            if _v == c:
                yield '', p[c]
            else:
                for s, v in self._travel(p[c]):     # TODO change recursive
                    yield c + s, v

    def search_prefix(self, pref):
        p = self._lookup(pref)
        if p:
            for s, v in self._travel(p):
                yield pref + s, v

    def in_trie(self, word):
        return self._lookup(word) is not None


def make_trie(words):
    trie = Trie()
    for word, v in words.iteritems():
        trie.insert(word, v)
    return trie


def show(s, trie):
    print 'search: %s...' % s
    for s1, v in trie.search_prefix(s):
        print '\t%s: %s' % (s1, v)


def test_freq():
    words = {'foo': 1, 'bar': 2, 'baz': 3, 'barz': 4}
    trie = make_trie(words)
    s = 'foo'
    assert trie.in_trie(s)
    trie.remove('baz')
    print trie.root
    show('ba', trie)


def test_reverse_index():
    sentences = ('python lang', 'hello world', 'network world',
                 'word and words')
    dic_index = {}
    for i, sen in enumerate(sentences):
        for w in sen.split():
            dic_index.setdefault(w, [])
            dic_index[w].append(i)
    trie = make_trie(dic_index)
    show('wor', trie)


if __name__ == '__main__':
    test_freq()
    test_reverse_index()
