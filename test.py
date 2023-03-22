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

# some imports require curses to be loaded already
try:
    from color import blue, red, green, black, color, pair
    from ast import Note, Integer, Operation
    from ast import Ast, Node
    import styles
    #from view import Display, Camera
    from activities.editor import Editor
    from activities.windows import Windows
    from activities.scroll import Scrollable
    from activities.menu import MenuNav

    from keyboard import KeyInterpreter
    from bindings.app import bindings

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
        self.stack = []
        self.activity = None
        self.running = False


        # load app-level events
        # typically, these can be used for global interruptions (pause the current activity and start a new one, abort and quit,...)
        self.keyboard = KeyInterpreter()
        #self.keyboard.on('q', self.quit)

        # deprecated
        #self.keyboard.parse(bindings)


    # events
    def getch(self):
        "wrapper for curses.screen.getch()"
        ch = self.screen.getch()
        if ch == curses.ERR:
            return None
        return ch


    # update
    def render(self):
        self.screen.erase()
        self.activity.render()
        self.screen.refresh()
        #self.view.update()

    # main loop
    def run(self, activity):
        #self.state = Editor(self)
        self.activity = activity
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

            self.activity.update(elapsed)
            self.screen.erase()
            self.activity.render()
            self.screen.refresh()


    # app life cycle
    def push(self, activity):
        self.stack.append(self.activity)
        self.activity = activity

    def pop(self):
        if len(self.stack):
            self.activity = self.stack.pop()
        else:
            self.quit()

    def quit(self):
        self.running = False

    def log(self, msg):
        with open('log', 'a') as f:
            f.write(msg)
            f.write('\n')




def main(screen):

    app = App(screen)
    #app.run(Windows(app))
    app.run(Editor(app))
    #app.run(Scrollable(app))
    #app.run(MenuNav(app))

    # TODO: add get_style() and check for situational styles like disabled, selected, bookmarked,...


try:
    main(screen)
finally:
    quit(screen)

