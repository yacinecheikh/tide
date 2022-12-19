class Trie:
    def __init__(self):
        self.content = {}

    def add(self, word):
        if len(word) == 1:
            self.content[word] = True
        else:
            ch = word[0]
            word = word[1:]
            self.content.setdefault(ch, Trie())
            self.content[ch].add(word)
