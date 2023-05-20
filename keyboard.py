"""
keyboard input interpreter


in all the program, <esc> is a global key binding to interrupt input sequences
"""


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
        "simple ascii sequence -> callback"
        self.bindings.write(seq, callback)

    def execute(self, ch):
        assert isinstance(ch, int)
        # TODO: use an activity to display the ascii code for the escape char
        # also check the get/set_escdelay(ms) in curses if escape is slow
        """
        if ch == KEY_ESC:
            pass
        else:
        """
        self.sequence.append(ch)
        if (callback := self.bindings.read(self.sequence)) is not None:
            callback()
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



def convert(sequence):
    # mutate the sequence
    # can call multiple times
    for i in range(len(sequence)):
        ch = sequence[i]
        if isinstance(ch, str):
            sequence[i] = ord(ch)
    return sequence




class KeyInterpreter2:
    """
    Input sequence interpreter (state machine)

    To allow curses special key constants, characters are encoded as numbers (ord(ch))
    """
    def __init__(self):
        # Trie
        self.bindings = {}
        # sub Trie
        self.state = self.bindings

        self.sequence = []
        # default behaviour when sequence is interrupted
        self.break_sequence = lambda: None

        # debug
        # use to produce warnings about conflicts
        # when writing new bindings
        # can be made real time if an embedded persistent binding/activity editor is made
        self.overrides = []


    def define(self, sequence, callback):
        """
        store a binding in the Trie

        sequence is a list of int
        (curses constants or ord(ch))
        """
        state = self.bindings
        for i, ch in enumerate(sequence[:-1]):
            # auto-convert char to ascii
            if isinstance(state.get(ch), Callable):
                self.overrides.append({
                    'conflict path': sequence[i:],
                    'new sequence': sequence,
                    'erased': state.get(ch),
                    'new binding': callback,
                })
                # override previous binding
                state[ch] = {}
            # state[ch] can be undefined, or an existing folder dict
            state.setdefault(ch, {})
            state = state[ch]
        # TODO: remove code duplication
        ch = sequence[-1]
        if isinstance(state.get(ch), Callable):
            # conflict with exact same sequence
            self.overrides.append({
                'conflict path': sequence,
                'erased': state[ch],
                'new binding': callback,
            })
        state[ch] = callback



    def execute(self, ch):
        # ch should be int
        # TODO: remove after tests
        assert isinstance(ch, int)

        self.sequence.append(ch)
        action = self.state.get(ch)
        if isinstance(action, dict):
            # nested binding
            self.state = action
        elif isinstance(action, Callable):
            action()
            # reset state
            self.state = self.bindings
            self.sequence = []
        elif action is None:
            self.break_sequence()
            self.state = self.bindings
            self.sequence = []


    # import bindings
    def parse(self, registry, head=[]):
        "recursively define() the bindings"
        for key, value in registry.items():
            if isinstance(key, str):
                prefix_length = len(key)
                for ch in key:
                    head.append(ord(ch))
            else:
                head.append(key)
                prefix_length = 1
            if isinstance(value, Callable):
                self.define(head, value)
            elif isinstance(value, dict):
                self.parse(value, head)
            for i in range(prefix_length):
                head.pop()
    

    def extend(self, parent):
        self.parse(parent.bindings)

    def on(self, *args):
        # 2 syntaxes
        # kb.on('seq' curses.KEY_DOWN, 'uence', callback)
        # @kb.on('sequence') ...
        decorator = not isinstance(args[-1], Callable)
        if decorator:
            parts = args
        else:
            parts = args[:-1]
        sequence = []
        for part in parts:
            if isinstance(part, int):
                sequence.append(part)
                continue
            # part is str
            for ch in part:
                sequence.append(ord(ch))
        if decorator:
            def decorator(f):
                self.define(sequence, f)
                return f
            return decorator
        else:
            callback = args[-1]
            self.define(sequence, callback)

