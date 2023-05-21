from ui import Control, Widget


class Notification(Control):
    # use a dedicated subwindow to delimit borders
    def __init__(self, window):
        self.window = window
        self.queue = []

    def add(self, control):
        pass



def Notifications(Widget):
    # TODO: when the camera moves, keep the notificatioss on the same spot ?
    # (ex: in a menu on the right
    # requires having a Display which does not fill the screen
    def __init__(self):
        super().__init__(self)
        self.rendering = []
        self.height = 2  # elements
        # cannot predict an element will be too long
        # any element could be 10 lines long and fill the screen
        # 
        self.lines = 3  # max lines before stopping
        self.duration = 3  # seconds

    def add(self, widget):
        self.queue.append({
            'time': 0,
            'element': widget,
        })

    def update(self, dt):
        for x in self.queue[:self.height][::-1]:
            # display the 3 first (lowest) nodes, from the top
            x['time'] += dt
            if x['time'] > 3:
                self.rendering.remove(x)
        # move from queue 
        while len(self.rendering) < 1 and len(self.queue):
            self.rendering.append({
                'time': 0,
                'element': self.queue.pop(0)
            })


    def render(self, screen, x, y):
        # x, y is for custom rendering
        # ignore when None ?
        pass

