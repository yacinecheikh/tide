from activities.base import Activity
from ui import Window, Box
from controls.base import Text
from controls.menu import Menu

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER


class MenuNav(Activity):
    def __init__(self, *args):
        super().__init__(*args)

        #self.keyboard.parse(bindings)
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
        self.menu = menu
        self.items['menu'] = Box(self.screen, 0, 0, menu)
        default_choice = menu.children[0]

        self.items['chosen'] = Box(self.screen, 12, 0, default_choice)


        kb = self.keyboard
        kb.on(self.up, KEY_UP)
        kb.on(self.down, KEY_DOWN)
        kb.on(self.select, '\n')
        kb.on(self.quit, 'q')

    def render(self):
        super().render()

    def up(self):
        self.items['menu'].content.up()
    
    def down(self):
        self.items['menu'].content.down()

    def select(self):
        choice = self.items['menu'].content.select()
        self.items['chosen'].content = choice


