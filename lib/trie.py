"""
stateless trie

used to handle input chord bindings
"""



# dict-based storage
class trie:
    """
    dict-based Trie

    for users:
        queries use a list as key (ab -> ['a', 'b'])
    for maintainers:
        keys are encoded in reverse order because muh efficiency
    """
    def __init__(self):
        self.storage = {}
    
    def get(self, key):
        path = key.copy()
        position = self.storage
        while path:
            position = position.get(path.pop())
            if position is None:
                return
        return position.get('value')

    def set(self, key, value):
        path = key.copy()
        position = self.storage
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
    t.set(list(str(x)), x)
    print(t.get(list(str(x))))
