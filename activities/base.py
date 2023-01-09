from keyboard import KeyInterpreter
#from bindings import


class Activity:
    def __init__(self, app):
        self.app = app
        self.keyboard = KeyInterpreter(app)
        # boxed controls
        self.items = {}

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
            x.render(self)
