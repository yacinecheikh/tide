"""
keyboard input interpreter


in all the program, <esc> is a global key binding to interrupt input sequences

"""

# TODO: for 1-character sequences (q to quit,...), there is still no way to bypass currently running sequences
# TODO: add support for more sequence breakers than <esc> ?

# or:
# TODO: add interrupts when an impossible sequence is being written


import curses
from typing import Callable

# TODO: remove using this
from ast import Note

from lib.trie import trie

# TODO: replace by special entry in dictionnary,
# for contextual sequence break behaviour override
#from actions import break_sequence


# TODO: convention: ESC is always used to break sequences
# TODO: @kb.on('seq', curses.char, 'seq') -> on(*args)
# TODO: design:
# app-level inputs can be defined with @app.kb.on()
# activity-level inputs can be defined with @app.activity.kb.on()
# each time a new activity is created, the events are inherited (but the inputs are not automatically redirected)
# other levels could be added, but the input receiver has to store all the event list
# there is no "event propagation" as it would conflict when multiple break_sequence() events are raised


class KeyInterpreter:

    def __init__(self):
        self.bindings = trie()
        self.sequence = []

    def define(self, seq, callback):
        "simple ascii sequence -> callback insertion"
        self.bindings.write(seq, callback)

    def execute(self, ch):
        assert isinstance(ch, int)
        # TODO: use an activity to display the ascii code for the escape char
        # also check the get/set_escdelay(ms) in curses if escape is slow
        """
        if ch == KEY_ESC and self.sequence:
            self.sequence = []
        else:
        """
        self.sequence.append(ch)
        queried = self.bindings.read(self.sequence)
        if isinstance(queried, bool):
            if not queried:  # incorrect sequence
                self.sequence = []
        else:
            queried()
            self.sequence = []

    # import bindings
    def extend(self, registry: trie, head=None):
        """
        define() all the bindings existing in the registry
        """
        for key, value in registry.items():
            self.define(key, value)

    # unfortunately, i could not find a proper way of using decorators to dynamically bind instance methods to local instances of KeyInterpreter without abusing inheritance
    # so you will have to define events with manual calls to on()
    def on(self, callback, *args):
        """
        example:
        kb.on(debug, KEY_DOWN, KEY_UP, KEY_ENTER, 'db')
        """
        sequence = []
        for part in args:
            if isinstance(part, int):
                sequence.append(part)
            else:
                for ch in part:
                    sequence.append(ord(ch))
        self.define(sequence, callback)

