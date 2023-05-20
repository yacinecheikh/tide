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
                return False

        val = position.get('value')
        # return a value or a boolean to indicate the presence of deeper values
        return (val if val is not None
                else len(position.keys()) - 1 > 0)

    def write(self, key, value):
        path = key.copy()
        position = self
        while path:
            ch = path.pop()
            position.setdefault(ch, {})
            position = position[ch]
        position['value'] = value

    def items(self, position=None, prefix=None):
        "for key, val in trie.items() generator"
        # recursive traversal, starting at self
        position = position or self
        prefix = prefix or []
        # can't use items()
        for key in position.keys():
            if key == 'value':
                value = position['value']
                key = prefix.copy()
                key.reverse()
                yield key, value
            else:
                # recursion
                prefix.append(key)
                yield from self.items(
                        position=position[key],
                        prefix=prefix)
                prefix.pop()


# TODO: move tests
"""
t = trie()

for x in range(100):
    t.write(list(str(x)), x)
    print(t.read(list(str(x))))

t.write([], "test")

for key, val in t.items():
    print(val, key)
"""
