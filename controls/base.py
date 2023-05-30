"""
multi-purpose primitives

Nodes are used for DOM-like structured data
Nodes should be subclassed to implement more behaviour, like syntax tree editing


Lines represent mutable, multipart strings.
The text can include blanks for transparency, and different styles for each part

Texts are just renderable line lists.
Texts can be used where Lines can.

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



class Line(Control):
    """
    multipart single-line text

    parts can be:
    -str (default style)
    -(str, 'default') for default (or line) style
    -(None, length) for (transparent) blanks
    -(text, style) for custom texts

    to change parts, you can access and edit line.parts
    """

    def __init__(self, *parts):
        self.parts = []
        for elt in parts:
            self.add(elt)
        self.style = styles.default

    def add(self, element):
        if isinstance(element, str):
            # default style
            element = (element, 'default')
        elif isinstance(element, int):
            # blank spaces
            element = (None, length)
        # (str, style) or (None, length)
        self.parts.append(element)

    def render(self, screen, x, y, default_style=None):
        if default_style is None:
            default_style = self.style
        for elt in self.parts:
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

        # width, height
        return x, y + 1


class Text(Control):
    """
    Kitchen sink, multipart text

    style: default style for all text elements without a specified style (can be modified after creation)
    lines: split lines for quick block indenting and/or line iteration

    this format allows both simple, multiline text
    and the usage of complex animated, non-ascii
    or transparent parts
    """

    def __init__(self, *lines):
        self.style = styles.default
        self.lines = []
        for line in lines:
            # ['spaced', 1, ('text', styles.blink)]
            # -> Line
            if not isinstance(line, Line):
                line = Line(*line)
            self.lines.append(line)


    # TODO: multiline text in constructor ?
    """
    def __init__(self, text: str, style=None):
        self.style = style or styles.default
        self.lines = []
        for line in text.split('\n'):
            self.lines.append(Text.Line(line))
    """

    def add(self, content, line='append'):
        # add a part to line <line>
        # create as many lines as needed (1 by default)
        if line == 'append':
            line = len(self.lines)

        while line >= len(self.lines):
            self.lines.append(Text.Line())

        # content is str, (str, style) or int
        self.lines[line].add(content)


    def render(self, display, x, y):
        width = 0
        height = 0
        for line in self.lines:
            w, _ = line.render(display, x, y, self.style)
            width = max(width, w)
            height += 1
        return width, height

