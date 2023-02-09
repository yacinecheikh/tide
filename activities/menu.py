from activities.base import Activity
from ui import Window, Box
from controls import Text, Menu
from bindings import menu as bindings


class MenuNav(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        self.keyboard.load(bindings)
        # hook for custom key bindings
        # instead of using the bindings.py module, local bindings can be set this way
        """
        self.keyboard.define({
            KEY_UP: menu.up, # self.up
        })
        """

        menu = Menu()
        menu.add(Text('choice1'))
        menu.add(Text('choice2'))
        menu.add(Text('choice3'))
        menu.add(Text('choice4'))
        self.items['menu'] = Box(self.screen, 0, 0, menu)
        default_choice = menu.children[0]

        self.items['chosen'] = Box(self.screen, 12, 0, default_choice)

    def render(self):
        super().render()

    def up(self):
        self.items['menu'].content.up()
    
    def down(self):
        self.items['menu'].content.down()

    def select(self):
        choice = self.items['menu'].content.select()
        self.items['chosen'].content = choice


