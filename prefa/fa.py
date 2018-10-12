class FiniteAutomata(object):
    """Finite Automata parent class.

    Can be initialized from a formatted source file, and stores the Automata
    in the form of a transition table. The file format and the storage
    structure is like:

                 a       b       c ~
        q0 {q0,q3} {q0,q1} {q0,q2} - ia
        q1       -       -      q3 -
        q2       - {q2,q3}       - -
        q3       -       -       - - a

    Notice that '-' must be used for an empty cell. '~' means epsilon here, 
    and is also an optional column. That is to say, epsilon is considered a
    normal symbol like 'a' / '0' here in parent class, and will be specially
    treated only in NFiniteAutomata child class. As a result, we can use '~'
    as a char symbol in a DFiniteAutomata, but cannot use '~' as a normal
    symbol in a NFiniteAutomata because it will be regarded as epsilon.

    Attributes:
        initial    - str , the initial state
        acceptings - set , set of acccepting states
        table      - dict, the transition table
        alphabet   - list, alphabet in sorted order
        states     - list, list of all states in sorted order
    """

    def __init__(self, input):
        self._initFromFile(input)   # Parent class can only init from file

    def _initFromFile(self, input_file):
        """Initializer for formatted source file.

        Reads in the formatted table in the source file, and constructs the
        Finite Automata correspondingly.

        Args:
            input_file - str, input source file name (/ path)
        """

        # Open the source file, and read in the first title line, which is
        # also the alphabet.
        f = open(input_file)
        self.alphabet = f.readline().split()
        # TODO(jose): Modify sort, let 'q2' < 'q10'
        self.alphabet.sort()

        # Read in the transition table line by line, and store it as a dict.
        self.table = {}
        self.states = []
        self.initial, self.acceptings = '-', set()
        for raw_line in f.readlines():
            line = raw_line.split()
            if (len(line) < len(self.alphabet) + 1):
                continue    # Jump over error lines
            state = line[0]
            self.states.append(state)
            self.table[state] = {}
            for j in range(len(self.alphabet)):
                dst = set(line[j+1].strip('}{ ').split(','))
                if dst == {'-'}:
                    self.table[state][self.alphabet[j]] = set()
                else:
                    self.table[state][self.alphabet[j]] = dst
            if len(line) == len(self.alphabet) + 2:
                if 'i' in line[-1]:     # 'i' in the end indicates initial
                    self.initial = state
                if 'a' in line[-1]:     # 'a' in the end indicates accepting
                    self.acceptings.add(state)
        f.close()

    def __str__(self):

        # Calculate formatted cells' width.
        state_len = 1 + max([len(state) for state in self.states])
        trans_len = 1
        for state in self.states:
            for a in self.table[state]:
                entry_len = len(str(stateSet(self.table[state][a])))
                if entry_len + 1 > trans_len:
                    trans_len = entry_len + 1

        # Put the first title line, i.e. the alphabet line.
        string = (state_len + 1) * ' '
        for a in self.alphabet:
            string += '{:>{width}} '.format(a, width = trans_len)
        string += '\n'

        # Append transition table line by line.
        for s in self.states:
            string += '{:<{width}} '.format(s, width = state_len)
            for a in self.alphabet:
                string+= ('{:>{width}} '
                          .format(str(stateSet(self.table[s][a])),
                                      width = trans_len))
            string += (state_len - 1) * ' '
            if s == self.initial:
                string += 'i'
            if s in self.acceptings:
                string += 'a'
            string += '\n'

        # Return the joined string
        return string

    def move(self, S, a):
        """Performs a transition move.

        From the initial state set S, given an input char symbol A, calculates
        the destination set that we can go to.

        Args:
            S - set, set of states to start from
            a - str, a char symbol in alphabet

        Returns:
            S_move - set, set of states that are moved to
        """
        # TODO(jose): Error checking
        S_move = set()
        for s in S:
            S_move |= self.table[s][a]
        return S_move

class stateSet(set):
    """Class which reloads the str() function for type Set.

    Reloads the printing format of type Set, so that empty set is '-', single
    element set is 'elem1', and multi elements set is '{elem1, elem2}' like
    the original.
    """

    def __str__(self):
        if len(self) == 0:
            return '-'
        elif len(self) == 1:
            return str(list(self)[0])
        else:
            string = '{'
            for elem in sorted(list(self)):
                string += str(elem) + ','
            string = string[:-1]
            string += '}'
            return string

if __name__ == '__main__':
    nfa = FiniteAutomata('../input/NFA')
    print(nfa.move({'q0', 'q1'}, 'c'))
    print(nfa)

    print(FiniteAutomata('../input/DFA'))
