class Node(object):
    def __init__(self, c, isleaf=False):
        self.c=c
        self.isleaf=isleaf
        self.children={}

class Trie(object):
    def __init__(self):
        self.root=Node('')

    def insert(self, word):
        if not word:
            return
        node =self.root
        for c in word:
            if c not in node.children:
                node.children[c]=Node(c)
            node = node.children[c]
        node.isleaf=True

    def travel(self, node):
        print node.c, node.isleaf and '|' or '',
        for child in node.children.values():
            self.travel(child)

    def candidates(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return 
            node = node.children[c]
        print node.c,node.children
        for node in node.children.values():
            print node.c
            self.travel(node)

words={
        'abc':2,
        'go':1,
        'golang':2,
        'xya':3,
    }

trie=Trie()
for word in words:
    trie.insert(word)
#trie.travel(trie.root)
for words in ('xxx', 'go'):
    trie.candidates('go')





