class DFSM:
    "Deterministic Finite State Machine"
    def __init__(self, states, symbols, start, accepting):
        self._transitions = {}
        self.start = start
        self.accepting = accepting
        self.state = start
        for state in states:
            self._transitions[state] = {s: None for s in symbols}

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

    def feed(self, input):
        for symbol in input:
            self.state = self._transitions[self.state][symbol]


class NFSM(DFSM):
    "Nondeterministic Finite State Machine"
    def __init__(self, states, symbols, start, accepting):
        super().__init__(states, symbols, start, accepting)
        self.state = self.closure([start])

    def closure(self, T):
        "States reached by following epsilon (empty string) edges from T"
        raise NotImplementedError

    def move(self, T, s):
        "States reached by following edges for symbol from set of states T"
        raise NotImplementedError

    def feed(self, symbols):
        for s in symbols:
            self.state = self.closure(self.move(self.state, s))

    @property
    def is_accepting(self):
        return len(set(self.accepting) & set(self.state)) > 0


def make_dfsm_from_table(table):
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
