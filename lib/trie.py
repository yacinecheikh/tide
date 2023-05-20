"""
stateless trie

used to handle input chord bindings
"""


class trie(dict):
    """
    dict-based Trie

    for users:
        queries use a list as key (ab -> ['a', 'b'])
    for maintainers:
        keys are encoded in reverse order because muh efficiency
    """
    
    # can't use get/set
    def read(self, key):
        path = key.copy()
        position = self  # self is the root dict
        while path:
            position = position.get(path.pop())
            if position is None:
                return
        return position.get('value')

    def write(self, key, value):
        path = key.copy()
        position = self
        while path:
            ch = path.pop()
            position.setdefault(ch, {})
            position = position[ch]
        position['value'] = value


    def items(self):
        # TODO: easily importable (key, value) generator
        pass

t = trie()

for x in range(100):
    t.write(list(str(x)), x)
    print(t.read(list(str(x))))
