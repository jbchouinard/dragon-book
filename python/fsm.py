from typing import AnyStr, List, Union

from aho_corasick import TaggedTrie, compute_failure_function


class DFSM:
    """Deterministic Finite State Machine"""

    def __init__(self, states=None, symbols=None, start=None, accepting=None):
        self._transitions = {}
        self.start = self.state = start
        self.accepting = accepting if accepting is not None else []
        self.symbols = symbols if symbols is not None else []
        if states is not None:
            for state in states:
                self._transitions[state] = {s: None for s in symbols}

    def add_state(self, state):
        self._transitions[state] = {}

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def add_transition(self, orig, symbol, dest):
        self._transitions[orig][symbol] = dest

    def add_transitions(self, orig, *transitions):
        for t in transitions:
            self.add_transition(orig, *t)

    def check(self):
        destinations = []
        for state in self._transitions.values():
            destinations += state.values()
        if any(d is None for d in destinations):
            return False
        return True

    @property
    def is_accepting(self):
        return self.state in self.accepting

    def feed(self, input_):
        for s in input_:
            t = self._transitions[self.state]
            if s in t:
                pass
            else:
                raise KeyError(
                    "there is no transition for symbol "
                    f"'{s}' from state '{self.state}'"
                )

    def reset(self):
        self.state = self.start


class NFSM(DFSM):
    """Nondeterministic Finite State Machine"""

    def __init__(self, states, symbols, start, accepting):
        super().__init__(states, symbols, start, accepting)
        self.state = self.closure([start])

    def closure(self, t):
        """States reachable by following epsilon (empty string) edges from t"""
        raise NotImplementedError

    def move(self, t, s):
        """States reachable by following edges for symbol s from set of
        states t """
        raise NotImplementedError

    def feed(self, symbols):
        for s in symbols:
            self.state = self.closure(self.move(self.state, s))

    @property
    def is_accepting(self):
        return len(set(self.accepting) & set(self.state)) > 0


def make_dfsm_from_table(table: AnyStr) -> DFSM:
    """
    Create deterministic finite state machine from a string representation
    of its transition table, like:
               a   b   c
        (0)    1   0   2
        [1]    0   1   2
         2     3   0   0
        [3]    0   1   2

     where (s) denotes the starting state, and [s] denotes an accepting state.
     [(s)], or ([s]), denotes that the starting state is accepting.
    """
    start = None
    accepting = []
    transitions = []
    states = []

    def read_state_symbol(sym):
        nonlocal start
        nonlocal accepting
        nonlocal symbols
        state = ''
        for letter in sym:
            if letter == '(':
                pass
            elif letter == '[':
                pass
            elif letter == ')':
                start = state
            elif letter == ']':
                accepting.append(state)
            else:
                state += letter
        states.append(state)
        return state

    lines = table.strip('\n\t ').split('\n')
    symbols = lines.pop(0).replace(' ', '').replace('\t', '')
    for line in lines:
        parts = [c for c in line.split(' ') if c not in ['', '\t']]
        state = read_state_symbol(parts.pop(0))
        for i in range(len(parts)):
            transitions.append((state, symbols[i], parts[i]))

    dfsm = DFSM(states, symbols, start, accepting)
    for t in transitions:
        dfsm.add_transition(*t)
    return dfsm


def make_kmp_dfsm(word: Union[AnyStr, List[AnyStr]]) -> DFSM:
    """Make a dfsm that accepts strings in .*word, based on KMP algorithm."""

    # Todo: compute failure function directly from FSM instead of having
    #       to construct two different data structures
    def b(s):
        return word[s]

    def l(s):
        return [b(s + 1), s + 1]

    trie = TaggedTrie()
    trie.create_root(0)
    for s in range(1, len(word) + 1):
        trie.create_node(s, word[0:s])
    f = compute_failure_function(trie)
    dfsm = DFSM()
    dfsm.add_state(0)
    for s in range(0, len(word)):
        dfsm.add_state(s + 1)
        dfsm.add_transition(s, b(s), s + 1)
        t = s
        while (t > 0):
            t = f[t]
            trans = [s] + l(t)
            if trans[1] not in dfsm._transitions[s]:
                dfsm.add_transition(*trans)
    return dfsm


if __name__ == '__main__':
    dfsm = DFSM([0, 1], 'ab', 0, [1])
    dfsm.add_transitions(0, ('a', 1), ('b', 0))
    dfsm.add_transitions(1, ('a', 0), ('b', 1))

    assert dfsm.check()
    dfsm.feed('bbba')
    assert dfsm.is_accepting

    table = (
        """
               a   b   c
        (0)    1   0   2
        [1]    0   1   2
         2     0   0   0
        """
    )
    dfsm2 = make_dfsm_from_table(table)

    assert dfsm2.check()
    assert not dfsm2.is_accepting
    dfsm2.feed('cabbbbbbbbcaa')
    assert dfsm2.is_accepting

    ndtable = (
        """
               a        b       c       epsilon
        (0)    {0,1}    {0}     {2}     {1}
         1     {0}      {1}     {1,2}   {}
        [2]    {}       {}      {}      {}
        """
    )
