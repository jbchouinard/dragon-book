#!/usr/bin/env python3
from typing import Dict

import attr


@attr.s
class TrieNode:
    tag = attr.ib(default=None)
    parent = attr.ib(default=None)
    children = attr.ib(default=attr.Factory(dict))
    accept = attr.ib(default=False)
    suffix = attr.ib(default=None)
    suffix_dist = attr.ib(default=0)

    def get(self, key):
        if not key:
            return self
        else:
            return self.children[key[0]].get(key[1:])

    def set(self, key, node):
        if len(key) == 1:
            self.children[key[0]] = node
            node.parent = self
        else:
            self.children[key[0]].set(key[1:], node)

    def get_child_key(self, child):
        return [k for (k, n) in self.children.items() if n is child][0]

    def get_branch_to(self):
        return self.parent.get_child_key(self)

    def get_key_iter(self):
        node = self
        key = []
        while node.parent:
            key.append(node.get_branch_to())
            node = node.parent
        return reversed(key)

    def get_key(self):
        return list(self.get_key_iter())

    def get_key_str(self):
        return ''.join(str(k) for k in self.get_key_iter())


class TaggedTrie:
    def __init__(self):
        self.tags = {}

    def create_root(self, tag):
        self.root = TrieNode(tag)
        self.tags[tag] = self.root

    def create_node(self, key, tag, accept=False):
        node = TrieNode(tag, accept)
        self.tags[tag] = node
        self.root.set(key, node)

    def get(self, key):
        return self.root.get(key)

    def get_by_tag(self, tag):
        return self.tags[tag]


class KeywordTrie:
    def __init__(self):
        self.root = TrieNode()
        self.current = self.root

    def get(self, key):
        return self.root.get(key)

    def add_word(self, word):
        node = self.root
        letters = list(word)
        while (letters and letters[0] in node.children):
            letter = letters.pop(0)
            node = node.children[letter]
        while (letters):
            letter = letters.pop(0)
            child = TrieNode(accept=(not letters))  # accept if last letter
            node.set(letter, child)
            node = child

    def match(self, letter):
        return letter in self.current.children.keys()

    def advance(self, letter):
        self.current = self.current.children[letter]

    @property
    def accepting(self):
        return self.current.accept

    def get_current_key(self):
        return self.current.get_key_str()

    def reset(self):
        self.current = self.root


class EndOfInput(Exception):
    pass


class ScannerError(Exception):
    def __init__(self, msg):
        super(ScannerError, self).__init__(msg)


class KeywordScanner:
    def __init__(self, dictionary, input):
        self.trie = KeywordTrie()
        for word in dictionary:
            self.trie.add_word(word)
        self.input = input
        self.pos = 0
        self.pos_match = 0
        self.pos_forward = 0
        self.input_length = len(input)
        self.end = 0 if input else 1

    def scan(self):
        self.trie.reset()
        matched_kw = False
        self.pos_forward = self.pos
        # Find the longest matching keyword
        while (not self.end and self.trie.match(self.input[self.pos_forward])):
            self.trie.advance(self.input[self.pos_forward])
            self.pos_forward += 1
            if self.pos_forward == self.input_length:
                self.end = True
            if self.trie.accepting:
                matched_kw = self.trie.get_current_key()
                self.pos_match = self.pos_forward

        if matched_kw:
            self.pos = self.pos_match
            return matched_kw
        elif self.end:
            raise EndOfInput
        else:
            raise ScannerError(
                ("Could not find a keyword in input at position %i, starting "
                 " with: %s...") % (
                    self.pos,
                    self.input[self.pos:self.pos+10]
                )
            )


def b(nodes):
    # Single node
    if isinstance(nodes, TrieNode):
        return nodes.get_branch_to()
    # Dict of children
    elif isinstance(nodes, dict):
        return list(nodes.keys())


def compute_suffix_links(root: TrieNode):
    """
    See wiki entry for Aho-Corasick algorithm for definition of suffix links
    with diagrams and everything.
    """
    open = []
    root.suffix = root
    for child in root.children.values():
        child.suffix = root
        child.suffix_dist = 1
        open.append(child)
    while open:
        node = open.pop(0)
        for child in node.children.values():
            t = node.suffix
            dist = node.suffix_dist
            while (t is not root and b(child) not in b(t.children)):
                t = t.suffix
                dist += t.suffix_dist
            if b(child) in b(t.children):
                t = t.children[b(child)]
            child.suffix = t
            child.suffix_dist = dist
            for c in child.children.values():
                open.append(child)
    return f


def compute_failure_function(tagged_trie: TaggedTrie) -> Dict[int, int]:
    """
    Compute suffix links for a tagged trie. Returns an explicit mapping of
    suffix links by tag.
    """
    f = {}
    open = []
    root = tagged_trie.root
    f[root.tag] = 0
    for child in root.children.values():
        f[child.tag] = 0
        open.append(child)
    while open:
        node = open.pop(0)
        for child in node.children.values():
            t = f[node.tag]
            while (t > 0 and b(child) not in b(tagged_trie.get_by_tag(t).children)):
                t = f[t]
            if b(child) in b(tagged_trie.get_by_tag(t).children):
                branch = tagged_trie.get_by_tag(t).children[b(child)]
                t = branch.tag
            f[child.tag] = t
            for c in child.children.values():
                open.append(child)
    return f


if __name__ == '__main__':
    trie = TaggedTrie()
    trie.create_root(0)
    trie.create_node('h', 1)
    trie.create_node('hi', 2)
    trie.create_node('his', 3, accept=True)
    trie.create_node('he', 4)
    trie.create_node('her', 5)
    trie.create_node('hers', 6, accept=True)
    trie.create_node('s', 7)
    trie.create_node('sh', 8)
    trie.create_node('she', 9, accept=True)

    assert trie.get('she').tag == 9, "error in getting node for 'she'"
    assert trie.get('hers').get_key_str() == 'hers', "error in getting key for 'hers'"

    f = compute_failure_function(trie)
    f_actual = {
        0: 0, 1: 0, 2: 0, 3: 7, 4: 0,
        5: 0, 6: 7, 7: 0, 8: 1, 9: 4
    }

    assert f == f_actual, "compute_failure_function is broken"

    compute_suffix_links(trie.root)
    for k, v in f_actual.items():
        assert trie.get_by_tag(k).suffix == trie.get_by_tag(v), "compute_suffix_links is broken"

    scanner = KeywordScanner([], '')
    try:
        scanner.scan()
        assert False, "expected an EnfOfInput exception"
    except EndOfInput:
        pass

    d = ['foo', 'bar', 'baz', 'foobar']
    input = 'bazbazbazbazbarfoobazbarfoobar'
    scanner = KeywordScanner(d, input)
    result = []
    while True:
        try:
            result.append(scanner.scan())
        except EndOfInput:
            break
    expected = ['baz', 'baz', 'baz', 'baz', 'bar', 'foo', 'baz', 'bar', 'foobar']
    assert result == expected, "error scanning input with KeywordScanner"

    input = 'why, but this should not parse!'
    scanner = KeywordScanner(d, input)
    try:
        scanner.scan()
        assert False, "expected a scanner error"
    except ScannerError:
        pass


