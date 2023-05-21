from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN

from activities.base import Activity
from ui import Window, Box
from controls.base import Text


class Scrollable(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        kb = self.keyboard
        kb.on(self.quit, 'q')
        kb.on(self.up, KEY_UP)
        kb.on(self.down, KEY_DOWN)
        kb.on(self.left, KEY_LEFT)
        kb.on(self.right, KEY_RIGHT)

        w = self.screen.w
        h = self.screen.h
        self.left = Window(self.screen, 0, 0, w // 2, h)
        self.right = Window(self.screen, w, 0, w - w // 2, h)

        abc = 'abcdefghijklmnopqrstuvwxyz' * 3
        t = Text(abc)
        self.items['left-text'] = Box(self.left, 0, 0, t)

    def render(self):
        super().render()

    
    def up(self):
        self.screen.move(0, -1)

    def down(self):
        self.screen.move(0, 1)

    def left(self):
        self.screen.move(-1, 0)

    def right(self):
        self.screen.move(1, 0)


