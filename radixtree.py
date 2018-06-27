#!/usr/bin/env python


class Node:
    def __init__(self):
        self.children = {}

    def isLeaf(self):
        return not self.children


class RadixTree():
    def __init__(self):
        self.root = Node()

    def _lookup(self, s):
        # Begin at the root with no elements found
        cur = self.root
        len_found = 0
        while cur and not cur.isLeaf() and len_found < len(s):
            nextNode = None
            for label, child in cur.children.iteritems():
                if s[len_found:].startswith(label):
                    nextNode = child
                    break
            if nextNode:
                cur = nextNode
                len_found += len(label)
            else:
                break
        return cur, len_found

    def insert(self, s):
        cur, len_found = self._lookup(s)
        if len_found == s:
            return
        pref = ''
        if not cur.isLeaf():
            for label, child in cur.children.iteritems():
                pref = com_pref(label, s[len_found:])
                if pref:
                    break
        if not pref:
            if len_found > 0:
                print '\t%s' %s[len_found:]
            cur.children[s[len_found:]] = Node()
        else:
            print '\tpref: %s' %pref
            newNode = Node()
            newNode.children[label[len(pref):]] = child
            cur.children[pref] = newNode
            cur.children.pop(label)
            newNode.children[s[len_found + len(pref):]] = Node()

    def search(self, s):
        cur, n = self._lookup(s)
        if n == len(s):
            yield s
            if not cur:
                return
            for label, child in cur.children.iteritems():
                if not child:
                    continue
                for s1 in self.search(label):
                    yield label + s1

    def delete(self, s):
        cur, n = self._lookup(s)
        if len(s) != n:
            return False
        # and cur.isLeaf():
            # cur
        return True
        # To delete a string x from a tree, we first locate the leaf representing x.
        # Then, assuming x exists, we remove the corresponding leaf node. If the parent
        # of our leaf node has only one other child, then that child's incoming label
        # is appended to the parent's incoming label and the child is removed.


def com_pref(s1, s2):
    for i, c in enumerate(s1):
        if i >= len(s2) or c != s2[i]:
            return s1[:i]
    return s1


def test():
    tree = RadixTree()
    for s in ('test', 'slow', 'water', 'tester', 'team', 'toast', 'slowly', 'testing', 'toaster'):
        print 'insert: %s' %s
        tree.insert(s)
    for s in ('ab', 'abe', 'ef', 'tester', 'slow'):
        print s, 'found: %s' %(','.join(tree.search(s)))


test()
