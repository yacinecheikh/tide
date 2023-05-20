
# TODO: partial queries (use the current state to move around nodes)

class trie:
    "wrapper interface"
    def __init__(self):
        self.root = Trie()
        # hooks, not needed
        self.state = self.root
        self.sequence = []  # path to the current state

    def set(self, key, value):
        # format the key for recursion
        if isinstance(key, int):
            key = [key]
        elif isinstance(key, str):
            key = [ord(ch) for ch in key]
        #key.reverse()

        key = self.parse(key)
        overrides = self.root.add(key, value)
        return overrides

    def get(self, ch):
        "react to a single character"
        ch = self.parse(ch)
        result = self.state.get(ch)
        if isinstance(result, Trie):
            self.state = result
            self.sequence.append(ch)
        elif result is not None:
            self.state = self.root
            self.sequence = []
            return result
        else:
            # query failed
            self.state = self.root
            self.sequence = []
            return None

    def parse(self, key):
        # convert to integer sequence
        if isinstance(key, int):
            key = [key]
        if isinstance(key, str):
            key = [ord(ch) for ch in key]
        return key


class Trie:
    """internal, optimized, recursive data structure

    nodes can be either values or sub-tries (check type)
    on path conflicts, remove the previous record and return the path and the contents of the erased record
    """
    def __init__(self):
        self.children = {}

    def add(self, sequence, value, path=None, overrides=None):
        # tracking override locations
        path = path or []
        overrides = overrides or []

        ch = sequence.pop()
        if len(sequence):
            if ch in self.children:
                # ch is defined as a value
                if not isinstance(self.children[ch], Trie):
                    # override
                    removed = self.children[ch]
                    overrides.append((path.copy(), removed))
                    self.children[ch] = Trie()
            else:
                self.children[ch] = Trie()
            # recursion
            overrides.extend(self.children[ch].add(sequence, value, path))
            return overrides
        else:
            if ch in self.children:
                # override
                removed = self.children[ch]
                overrides.append((path.copy(), removed))
            self.children[ch] = value

        return overrides

    def get(self, sequence):
        "None if the value is not defined"
        ch = sequence.pop()
        if ch not in self.children:
            # failed query
            return
        elt = self.children[ch]
        if len(sequence):
            return (elt if isinstance(elt, Trie)
                    else None)
        else:
            # elt can be a Trie (partial query)
            return elt

t = trie()

for x in range(10):
    t.set(str(x), x)
    print(t.get(str(x)))
