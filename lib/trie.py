"""
stateless trie

used to handle input chord bindings
"""

class trie:
    "wrapper interface over recursive Trie"
    def __init__(self):
        self.root = Trie()
        # hooks, not needed
        """
        self.state = self.root
        self.sequence = []  # path to the current state
        """

    def set(self, key, value):
        # keys are stored in reverse order
        #key.reverse()

        key = self.format(key)
        self.root.set(key, value)

    def get(self, key):
        key = self.format(key)
        return self.root.get(key)

    """
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
    """

    def format(self, key):
        # convert to integer sequence for recursive queries
        # query keys are destroyed in the process
        if isinstance(key, int):
            key = [key]
        if isinstance(key, str):
            key = [ord(ch) for ch in key]
        return key


class Trie:
    """
    internal recursive data structure

    silently overrides older definitions
    """
    def __init__(self):
        self.children = {}
        self.value = None

    def set(self, path, value):
        if path:
            ch = path.pop()
            self.children.setdefault(ch, Trie())
            self.children[ch].set(path, value)
        else:
            self.value = value

    def get(self, path):
        # None is used for undefined values
        if path:
            ch = path.pop()
            node = self.children.get(ch)
            if node is not None:
                return node.get(path)
        else:
            return self.value

t = trie()

for x in range(100):
    t.set(str(x), x)
    print(t.get(str(x)))
