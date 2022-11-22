import curses



"""
tips:
-use init() and quit()
(do not use the wrapper from curses)
-use getch() and check null-results with == curses.ERR
-use color.py
"""



def init():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    screen.nodelay(True)
    curses.curs_set(False)
    curses.start_color()
    curses.use_default_colors()
    return screen


def quit(screen):
    curses.nocbreak()
    screen.keypad(False)
    screen.nodelay(False)
    curses.echo()
    curses.curs_set(True)
    curses.endwin()


# color has to be imported after curses.start_color()

screen = init()

try:
    from color import blue, red, green, black, color, pair
    from ast import Note, Integer, Operation
    from ast import Ast, Node
    import styles
    from view import Display, Camera
except Exception as e:
    quit(screen)
    raise e


def main(screen):
    screen.clear()

    # TODO: add get_style() and check for situational styles like disabled, selected, bookmarked,...

    """
    body:
      loop:
        sticky
        print
    """

    display = Display(screen)
    camera = Camera(display)

    root = Node()
    ast = Ast(root)
    root.text = 'body:'
    loop = Node()
    loop.text = 'loop:'
    note = Note('sticky')
    loop.add(note)
    instruction = Node()
    instruction.text = 'print'
    loop.add(instruction)
    root.add(loop)
    n = Integer(38)
    m = Integer(48)
    op = Operation('+', n, m)
    root.add(op)

    ast.render(display)
    camera.update()

    screen.refresh()
    while True:
        ch = screen.getch()
        if ch != curses.ERR:
            break

        screen.refresh()

try:
    main(screen)
finally:
    quit(screen)

