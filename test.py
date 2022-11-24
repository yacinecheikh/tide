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


class App:
    '''
    Singleton antipattern

    needed to give control over the application from the key binding callbacks

    also used in video games
    '''
    def __init__(self, screen):
        self.screen = screen
        self.display = Display(screen)
        self.view = Camera(self.display)

    def run(self):
        self.running = True
        self.screen.clear()
        
        root = Node()
        ast = Ast(root)
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

        self.view.move(0, 0)


        while self.running:
            ch = self.screen.getch()
            if ch != curses.ERR:
                root.add(Note(chr(ch)))
            if ch == curses.KEY_UP:
                self.view.move(0, -1)
            if ch == curses.KEY_DOWN:
                self.view.move(0, 1)
            if ch == curses.KEY_LEFT:
                pass
            if ch == ord('q'):
                self.running = False

            ast.render(self.display)
            self.view.update_view()



def main(screen):

    App(screen).run()

    # TODO: add get_style() and check for situational styles like disabled, selected, bookmarked,...


try:
    main(screen)
finally:
    quit(screen)

