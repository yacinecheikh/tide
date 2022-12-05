import curses


"""
api:

classes for each AST construct
-if/else/elseif (cond)
-comment
-function
-import
-expression (recursive value)
-literals (num, str, table, array, boolean)
-calls
-operators (+-, */, #)


additional abstractions:
-closures (static variable, 'internal memory')
-classes (in lua)
-> attributes, methods, type of class
-inline "override operator", "add new method" style operations
(setmetatable + metatable definition)
-snippets (templates with specified values and placeholders)


additional info:
-comment
-docstrings
-disabled (commented code)
-for vars and funcs: type hints (can include dependant types type checker)






DRY api:
-base Node
-inline and multiline texts
(used for block delimiters)
-children container
-expressions: inline rendering

choices:
-mixins
-composition of high level (and flexible) components
"""

from color import pair, grey, lightgrey, black, white
import color as c

import styles
import settings as s


class Ast:
    def __init__(self, root = None):
        self.root = root
        self.selected = []
        self.bookmarks = {}
        #self.select(root)

    def select(self, node):
        node.selected = True
        self.selected.append(node)

    def unselect(self, node):
        self.selected.remove(node)
        node.selected = False

    def bookmark(self, i, node):

        if key in self.bookmarks:
            self.bookmarks[key].bookmarked -= 1
        node.bookmarks += 1
        self.bookmark[key] = node

    def render(self, screen, x, y):
        if self.root is not None:
            self.root.render(screen, x, y)

    def generate(self):
        pass



class Node:
    "Elements of an abstract tree"
    def __init__(self):
        # generic properties
        self.style = styles.default
        self.docstring = None  # any AST node can be documented
        self.enabled = True

        # user navigation
        # generic focus cursor
        self.selected = False
        # used for custom rendering
        # number of bookmarks leading to this node
        self.bookmarks = 0

        # DOM-like tree
        self.parent = None
        self.children = []

        # text content
        self._text = None
        self.lines = []


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.lines = text.split('\n')

    def add(self, child):
        child.parent = self
        self.children.append(child)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def format(self):
        if self.selected:
            return styles.cursor
        if self.enabled is False:
            return styles.disabled
        if self.selected:
            return styles.cursor

        if self.bookmarks:
            return styles.bookmark


        return self.style


    def render(self, screen, x = 0, y = 0):
        c = 0
        for line in self.lines:
            screen.add(x, y + c, line, self.style)
            c += 1
        for child in self.children:
            c += child.render(screen, x + s.indent, y + c)
        return c

    def rendertext(self, screen, x, y, text):
        pass
    def renderchild(self, screen, x, y, child):
        pass



# TODO: write nodes


class Integer(Node):
    def __init__(self, value):
        super().__init__()
        self.text = str(value)
        self.value = value



class Operation(Node):
    def __init__(self, operator, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.op = operator
        self.text = f'{left.text} {operator} {right.text}'  


class Note(Node):
    "True comments. Can be moved, disabled when not useful, or just read"
    def __init__(self, note=''):
        super().__init__()
        self.text = note
        self.style = styles.comment

    def render(self, screen, x, y):
        for i, line in enumerate(self.lines):
            screen.add(x, y + i, line, self.style)
        return i + 1


class ImportList(Node):
    def __init__(self, paths):
        pass

class Expr:
    pass

class Number(Expr):
    def __init__(self, value):
        self.value = value

class String(Expr):
    def __init__(self, value):
        self.value = value

class Bool(Expr):
    pass

class Cond(Expr):
    # if/elseif chained
    def __init__(self, switchlist):
        for (boolexpr, action) in switchlist:
            pass

# not needed, equivalent to (expr)
class NestedExpr(Expr):
    def __init__(self, content):
        self.value = content

class Unary(Expr):
    def __init__(self, operator, arg: Expr):
        self.op = operator
        self.arg = arg


class VarDef(Node):
             # should contain "implement" runtime checker
             # as well as "type"
     pass
