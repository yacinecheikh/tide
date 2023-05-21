from controls.base import Node, Text


class ItemList(Node):
    def __init__(self):
        super().__init__(indent = 0)
    

class Menu(ItemList):
    "chosable items"
    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.cursor = 0
        self.cursor_text = Text(' <-')

        self.text = None

    def gentext(self):
        # cursor after first line
        # pb: elements cannot be converted to Text
        # (especially if they change over time)
        pass

    def render(self, screen, x, y):
        # w, h rendering
        height = 0
        width = 0
        for i in range(len(self.children)):
            item = self.children[i]
            w, h = item.render(screen, x + self.indent, y + height)
            if self.cursor == i:
                self.cursor_text.render(screen, x + w + self.indent, y + height)
            height += h
            width = max(w, width)
        return width, height

    def select(self):
        return self.children[self.cursor]

    def down(self):
        self.cursor += 1
        if self.cursor >= len(self.children):
            self.cursor = 0

    def up(self):
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = len(self.children) - 1


class FileNav:
    pass
