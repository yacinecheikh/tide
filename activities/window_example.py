from ui import Window, ScreenWindow
from math import ceil
from activities.base import Activity


class Windows(Activity):
    def __init__(self, *args):
        super().__init__(*args)
        self.screen = ScreenWindow(self.app.screen)

        # template code for split coordinates
        x, y, w, h = 0, 0, self.screen.w // 2, self.screen.h // 2
        self.topleft = Window(self.screen, x, y, w, h)
        x, y = self.topleft.w, 0
        # may include odd widths
        w = self.screen.w - self.topleft.w
        self.topright = Window(self.screen, x, y, w, h)


        # split in 4
        x, y = 0, self.topleft.h
        w = self.topleft.w
        h = self.screen.h - self.topleft.h
        self.bottomleft = Window(self.screen, x, y, w, h)

        x, y = self.bottomleft.w, self.topright.h
        w = self.screen.w - self.bottomleft.w
        h = self.screen.h - self.topright.h
        self.bottomright = Window(self.screen, x, y, w, h)


    def render(self):
        # long enough to get trimmed by the subscreens
        abc = 'abcdefghijklmnopqrstuvwxyz' * 2
        #self.screen.write(0, 0, abc)
        self.topleft.write(0, 0, abc)
        for i in range(self.topleft.h):
            self.topleft.write(0, i, abc[i])
        self.topright.write(0, 0, abc)
        for i in range(self.topright.h):
            self.topright.write(0, i, abc[i])
        self.bottomleft.write(0, 0, abc)
        for i in range(self.bottomleft.h):
            self.bottomleft.write(0, i, abc[i])
        self.bottomright.write(0, 0, abc)
        for i in range(self.bottomright.h):
            self.bottomright.write(0, i, abc[i])

