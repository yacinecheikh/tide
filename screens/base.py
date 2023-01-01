from keyboard import KeyInterpreter
#from bindings import


class Screen:
    def __init__(self, app):
        self.app = app
        self.keyboard = KeyInterpreter()
        self.items = {}


    def update(self, dt):
        for x in self.items.values():
            x.update(dt)

        ch = self.app.getch()
        if ch is not None:
            self.keyboard.execute(ch)

    def render(self, screen):
        for x in self.items.values():
            x.render(self, screen)
