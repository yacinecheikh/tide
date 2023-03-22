"""
AST editor
"""


from ast import Ast, Node, Note, Integer, Operation
from activities.base import Activity
from ui import Window, Box


class Editor(Activity):
    def __init__(self, *args):
        super().__init__(*args)
        self.ast = Ast()

        kb = self.keyboard
        kb.on('q', self.quit)
        # debug-print, debug-debug
        kb.on('dp', self.print)
        kb.on('ic', self.insert_comment)


        root = Node()
        self.ast.root = root
        self.ast.select(root)
        self.framerate = Note()
        self.input = Note()
        root.add(self.framerate)

        root.text = 'body:'
        loop = Node()
        loop.text = 'loop:'
        loop.add(Note('sticky'))
        instruction = Node()
        instruction.text = 'print'
        loop.add(instruction)
        root.add(loop)
        n = Integer(38)
        m = Integer(48)
        op = Operation('+', n, m)
        root.add(op)

        framerate = Note('')
        root.add(framerate)



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

    def print(self):
        ch = self.keyboard.sequence[0]
        # can only be called when in editor state
        self.ast.root.add(Note(str(ch)))

    def insert_comment(self):
        for node in self.ast.selected:
            note = Note()
            node.add(note)
            self.ast.unselect(node)
            self.ast.select(note)
