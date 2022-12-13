import curses
from datetime import datetime
from time import sleep, time



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
    from screens.editor import Editor
    from screens.windows import Windows

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
        # Display should be used for scrollable subscreens
        #self.display = Display(screen)
        #self.view = Camera(self.display)

        #self.view.move(0, 0)
        #self.screen = screen
        self.statestack = []
        self.state = None
        self.running = False



    def getch(self):
        "wrapper for curses.screen.getch()"
        ch = self.screen.getch()
        if ch == curses.ERR:
            return None
        return ch


    def render(self):
        self.screen.erase()
        self.state.render()
        self.screen.refresh()
        #self.view.update()

    def run(self, state):
        #self.state = Editor(self)
        self.state = state
        self.running = True


        # AST init code
        """
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
        """



        self.render()

        dt = 1 / 60
        old = time()


        while self.running:
            # slow framerate down to 1/dt
            t = time()
            elapsed = t - old
            old = t

            if elapsed < dt:
                sleep(dt - elapsed)
                elapsed = dt

            self.state.update(elapsed)
            self.screen.erase()
            self.state.render()
            self.screen.refresh()




def main(screen):

    app = App(screen)
    app.run(Windows(app))
    #app.run(Editor(app))

    # TODO: add get_style() and check for situational styles like disabled, selected, bookmarked,...


try:
    main(screen)
finally:
    quit(screen)

