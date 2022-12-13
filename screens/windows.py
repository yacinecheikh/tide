from graphics import Window, ScreenWindow
from math import ceil


class Windows:
    def __init__(self, app):
        self.app = app
        self.screen = ScreenWindow(app.screen)

        x, y, w, h = 0, 0, self.screen.w // 2, self.screen.h // 2
        self.topleft = Window(self.screen, x, y, w, h)
        x, y = self.topleft.x + 1, 0
        w, y = self.screen.w - self.topleft.w, self.screen.h // 2
        self.topright = Window(self.screen, x, y, w, h)
        
    def update(self, dt):
        pass    

    def render(self):
        abc = 'abcdefghijklmnopqrstuvwxyz'
        self.topleft.write(0, 0, abc)
        self.topright.write(0, 0, abc)
