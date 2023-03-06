from keyboard import KeyInterpreter
from ui import ScreenWindow
#from bindings import


class Activity:
    def __init__(self, app):
        self.app = app
        self.keyboard = KeyInterpreter()
        self.keyboard.extend(app.keyboard)
        # boxed controls
        self.items = {}
        # app.screen is the terminal screen
        # activity.screen is a Window wrapper
        self.screen = ScreenWindow(app.screen)

        """ # hook for auto-resize
        self.windows = {
            'main': ScreenWindow(app.screen)
        }
        """


    def update(self, dt):
        # TODO: refresh window sizes if screen size changes

        for x in self.items.values():
            x.update(dt)

        ch = self.app.getch()
        if ch is not None:
            self.keyboard.execute(ch)

    def render(self):
        # TODO: support subwindows
        # -> use Boxes to use a window as screen and avoid explicit repetition when rendering
        for x in self.items.values():
            x.render()
