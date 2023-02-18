"""
AST editor
"""


from ast import Ast, Node, Note
from bindings import editor as edit_bindings
from activities.base import Activity
from ui import Window, Box


class Editor(Activity):
    def __init__(self, *args):
        super().__init__(*args)
        self.ast = Ast()

        self.keyboard.parse(edit_bindings)


        root = Node()
        self.ast.root = root
        self.ast.select(root)
        self.framerate = Note()
        self.input = Note()
        root.add(self.framerate)



        self.items['ast'] = Box(self.screen, 0, 0, self.ast)

    def render(self):
        #self.ast.render(self.window, 0, 0)
        pass

    def update(self, dt):
        self.framerate.text = str(1 / dt)
        ch = self.app.getch()
        if ch is not None:
            self.keyboard.execute(ch)
            self.input.text += str(ch)
