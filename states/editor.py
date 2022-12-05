"""
AST editor
"""


from ast import Ast, Node, Note
from keyboard import Interpreter
from bindings import editor as edit_bindings


class Editor:
    def __init__(self, app):
        self.app = app
        self.ast = Ast()

        self.keyboard = Interpreter(app)
        self.keyboard.load(edit_bindings)


        root = Node()
        self.ast.root = root
        self.ast.select(root)
        self.framerate = Note()
        self.input = Note()
        root.add(self.framerate)

    def render(self):
        self.ast.render(self.app.display, 0, 0)
        #app.render() does the actual rendering

    def update(self, dt):
        self.framerate.text = str(1 / dt)
        ch = self.app.getch()
        if ch is not None:
            self.keyboard.execute(ch)
            self.input.text += str(ch)
