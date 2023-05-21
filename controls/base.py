"""
multi-purpose primitives

Nodes are used for DOM-like structured data
Nodes should be subclassed to implement more behaviour, like syntax tree editing

Texts are multipart areas that render (static) data.
Texts can handle color and can be dynamically changed their data.
Texts are currently very bloat, but they provide an api to render about anything.
Internally, Texts use Lines of (style, text) to model a graphical rendering. This means Texts can have gaps and different styles
"""


import styles
import settings

from ui import Control


# can be extended for usage in AST, file navigation menus,...
# inherited control should manage their own indent
class Node(Control):
    """
    Generic purpose Node tree
    (element of an objet oriented linked tree)

    Nodes only manage the indentation of their children
    (they don't have their own rendering)

    To manage style and other properties, go through a node tree to process non-Node children
    """
    def __init__(self, indent = settings.indent):
        # DOM-like tree
        self.parent = None
        self.children = []

        # default setting
        self.indent = indent


    def add(self, child):
        child.parent = self
        self.children.append(child)


    def update(self, dt):
        for item in self.children:
            item.update(dt)


    def render(self, screen, x = 0, y = 0):
        # w, h rendering
        height = 0
        width = 0
        for item in self.children:
            w, h = item.render(screen, x + self.indent, y + height)
            height += h
            width = max(w, width)
        return width, height


class Text(Control):
    """
    Kitchen sink, multipart text

    style: common style for all text parts without a dedicated style (can be modified after creation)
    lines: split lines for quick block indenting and/or line iteration

    Lines are renderable objects. Can contain subparts with a dedicated style, and use the parent text style as default

    this format allows both simple, multiline text
    and the usage of complex animated, non-ascii
    or transparent parts
    """


    class Line:
        def __init__(self, *parts):
            #self.style = default_style
            self.contents = []
            for elt in parts:
                self.add(elt)

        def add(self, element):
            # auto-format str to (str, style)
            if isinstance(element, str):
                element = (element, 'default')
            # item is (str, style) or (None, length)
            self.contents.append(element)

        def render(self, screen, x, y, default_style):
            for elt in self.contents:
                text, param = elt
                if text is None:
                    # transparency (blank spaces)
                    x += param
                else:
                    # override default style
                    if param == 'default':
                        style = default_style
                    else:
                        style = param
                    screen.write(x, y, text, style)
                    x += len(text)

            # width
            return x

    # TODO: constructor styles
    # Text()
    # Text(style = style)
    # Text(multiline)
    # Text((str1, style), (str2, style),...)


    def __init__(self, text: str, style=None):
        self.style = style or styles.default
        # line contents are str, (str, style),
        # or (None, length) for transparent parts


        # TODO(maybe):
        # the constructor only takes a single string
        # could change later
        # for now, Line is internal
        self.lines = []
        for line in text.split('\n'):
            self.lines.append(Text.Line(line))

    def add(self, content, line='append'):
        if line == 'append':
            line = len(self.lines)

        while line >= len(self.lines):
            self.lines.append(Text.Line())

        # content is str, (str, style) or (None, length)
        self.lines[line].add(content)


    def render(self, display, x, y):
        width = 0
        height = 0
        for line in self.lines:
            w = line.render(display, x, y, self.style)
            width = max(width, w)
            height += 1
        return width, height

