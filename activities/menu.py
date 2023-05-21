from activities.base import Activity
from ui import Window, Box
from controls.base import Text
from controls.menu import Menu, MenuEvents

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER


class MenuNav(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        menu = Menu()
        menu.add(Text('choice1'))
        menu.add(Text('choice2'))
        menu.add(Text('choice3'))
        menu.add(Text('choice4'))
        self.menu = menu
        self.items['menu'] = Box(self.screen, 0, 0, menu)
        default_choice = menu.children[0]

        self.items['chosen'] = Box(self.screen, 12, 0, default_choice)



        self.menuevents = MenuEvents(
                menu,
                confirm = self.select,
                cancel = self.quit)
        # events are sent to self.keyboard
        self.mainevents = self.keyboard
        self.keyboard = self.menuevents


    def render(self):
        super().render()

    def select(self, choice):
        self.items['chosen'].content = choice


