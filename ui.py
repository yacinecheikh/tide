import curses


"""
api:
Node: contains (vertically)  renderable things
Text: formatted, multipart text
"""

from color import pair, grey, lightgrey, black, white
import color as c

import styles
import settings




class Text:
    """
    Kitchen sink text

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
            self.lines.append(Line(line))

    def add(self, content, line='append'):
        if line == 'append':
            line = len(self.lines)

        while line >= len(self.lines):
            self.lines.append(Line())

        # content is str, (str, style) or (None, length)
        self.lines[line].add(content)


    def render(self, screen, x, y):
        for line in self.lines:
            line.render(screen, x, y, self.style)
            y += 1


# can be extended for usage in AST, file navigation menus,...
class Node:
    """
    Generic purpose Node tree
    (element of an objet oriented linked tree)

    for custom rendering and data/node mixing, use children to mix items and nodes

    Nodes only manage the indentation of their children
    (they don't have their own rendering)

    To manage style and other properties, go through a node tree to process non-Node children
    """
    def __init__(self):
        # DOM-like tree
        self.parent = None
        self.contents = []
        self.items = []
        sely.load = []
        self.data = []
        self.children = []

        # default setting
        self.indent = settings.indent


    def add(self, child):
        child.parent = self
        self.children.append(child)


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
        for item in self.children:
            if isinstance(item, Node):
                 c += item.render(screen, x + self.indent, y + c)
            else:
                c += item.render(screen, x, y + c)
        return c

