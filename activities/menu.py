from activities.base import Activity
from ui import Window, Box
from controls import Text, Menu
from bindings import menu as bindings


class MenuNav(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        self.keyboard.load(bindings)

        menu = Menu()
        menu.add(Text('choice1'))
        menu.add(Text('choice2'))
        self.items['menu'] = Box(self.screen, 0, 0, menu)

        self.items['chosen'] = Box(self.screen, 0, 5, Text(''))

    def render(self):
        super().render()

    def up(self):
        self.items['menu'].content.up()
    
    def down(self):
        self.items['menu'].content.down()

    def select(self):
        choice = self.items['menu'].content.select()
        self.items['chosen'].content = choice


