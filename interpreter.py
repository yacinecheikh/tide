import curses
from typing import Callable

from ast import Note

"""
bindings = {
    'd': {
        'p': lambda: print('debug print test')
    }
}
"""


def slide_right(app, seq):
    app.view.move(1, 0)

def slide_left(app, seq):
    app.view.move(-1, 0)

def slide_up(app, seq):
    app.view.move(0, -1)

def slide_down(app, seq):
    app.view.move(0, 1)

def quit_app(app, seq):
    app.running = False

def default(app, seq):
    ch = seq[0]
    app.display.element.add(Note(ch))

def break_sequence(app, seq):
    app.display.element.add(Note(str(seq) + 'not found'))




# TODO: move this in a default_bindings file
default_shortcuts = {
    curses.KEY_UP: slide_up,
    ord('q'): quit_app,


    'd': {
        'p': lambda app, seq: print('debug print test')
    },
    'dp': lambda app, seq: print('debug 2')
}





# TODO: test everything
class Interpreter:
    def __init__(self, app):
        self.app = app

        self.bindings = {}
        self.state = self.bindings
        self.sequence = []
        self.overrides = []

    def define(self, seq, callback):
        current_level = self.bindings
        for i, ch in enumerate(seq[:-1]):
            if isinstance(ch, str):
                # auto-convert from chr to ord
                # using ord() integers allows using curses special key constants
                ch = ord(ch)
            if isinstance(current_level.get(ch), Callable):
                # already defined -> keep track of previous bindings for later real time tests
                self.overrides.append((seq[i:], current_level[ch]))
                current_level[ch] = {}
            current_level.setdefault(ch, {})
            current_level = current_level[ch]
        ch = seq[-1]
        if current_level.get(ch) is not None:
            self.overrides.append((seq, current_level[ch]))
        current_level[ch] = callback


    def execute(self, ch):
        self.sequence.append(ch)
        action = self.state.get(ch)
        if isinstance(action, dict):
            # nested binding
            self.state = action
        elif isinstance(action, Callable):
            action(self.app, self.sequence)
            # reset state
            self.state = self.bindings
            self.sequence = []
        elif action is None:
            # reset state and call break()
            self.state = self.bindings
            self.bindings['bread-sequence'](self.sequence)
            self.sequence = []

    def load(self, d, sequence_head=[]):
        for key, value in d.items():
            if isinstance(key, str) and len(key) > 1:
                # compact notation (multi-char string)
                sequence_head.extend(key)
            else:
                # str or integer, handled by define()
                sequence_head.append(key)
            if isinstance(value, Callable):
                self.define(sequence_head, value)
            elif isinstance(value, dict):
                self.load(value, sequence_head)
            sequence_head.pop()
    





#define({}, 'dp', lambda: print('debug print test')
