from activities.base import Activity
from ui import Window, Box
from controls import Text
from bindings import scroll as bindings


class Scrollable(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        self.keyboard.load(bindings)

        w = self.screen.w
        h = self.screen.h
        self.left = Window(self.screen, 0, 0, w // 2, h)
        self.right = Window(self.screen, w, 0, w - w // 2, h)

        abc = 'abcdefghijklmnopqrstuvwxyz' * 3
        t = Text(abc)
        self.items['left-text'] = Box(self.left, 0, 0, t)

    def render(self):
        super().render()


