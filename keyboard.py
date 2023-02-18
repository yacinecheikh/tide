"""
keyboard input interpreter
"""


import curses
from typing import Callable

# TODO: remove using this
from ast import Note

# TODO: replace by special entry in dictionnary,
# for contextual sequence break behaviour override
from actions import break_sequence


# TODO: convention: ESC is always used to break sequences
# TODO: @kb.on('seq', curses.char, 'seq') -> on(*args)
# TODO: design:
# app-level inputs can be defined with @app.kb.on()
# activity-level inputs can be defined with @app.activity.kb.on()
# each time a new activity is created, the events are inherited (but the inputs are not automatically redirected)
# other levels could be added, but the input receiver has to store all the event list
# there is no "event propagation" as it would conflict when multiple break_sequence() events are raised



def convert(sequence):
    # mutate the sequence
    # can call multiple times
    for i in range(len(sequence)):
        ch = sequence[i]
        if isinstance(ch, str):
            sequence[i] = ord(ch)
    return sequence




class KeyInterpreter:
    """
    Input sequence interpreter (state machine)

    To allow curses special key constants, characters are encoded as numbers (ord(ch))
    """
    def __init__(self, app):
        self.app = app
        # Trie
        self.bindings = {}
        # sub Trie
        self.state = self.bindings

        self.sequence = []
        self.break_sequence = None  # callback

        # event redirection
        self.redirect = None

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

        # redirect events
        if self.redirect is not None:
            self.redirect.execute(ch)
            return

        self.sequence.append(ch)
        action = self.state.get(ch)
        if isinstance(action, dict):
            # nested binding
            self.state = action
        elif isinstance(action, Callable):
            action(self.app)
            # reset state
            self.state = self.bindings
            self.sequence = []
        elif action is None:
            if self.break_sequence is not None:
                self.break_sequence(self.app)
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
        # @kb.on('seq\nuence') ...
        decorator = not isinstance(args[-1], Callable)
        if decorator:
            parts = args[:-1]
        else:
            parts = args
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




class KeyInterpreter2:
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
        # TODO: find why ord(ch) has never been necessary, test if using it breaks
        current_level[ch] = callback


    def execute(self, ch):
        # ch should be int
        self.sequence.append(ch)
        action = self.state.get(ch)
        if isinstance(action, dict):
            # nested binding
            self.state = action
        elif isinstance(action, Callable):
            action(self.app)
            # reset state
            self.state = self.bindings
            self.sequence = []
        elif action is None:
            # reset state and call break()
            self.state = self.bindings
            break_sequence(self.app)
            #self.bindings['break-sequence'](self.sequence)
            self.sequence = []

    def load(self, d, sequence_head=[]):
        "recursively define the bindings"
        for key, value in d.items():
            if isinstance(key, str):
                prefix_length = len(key)
                for ch in key:
                    sequence_head.append(ord(ch))
            else:
                sequence_head.append(key)
                prefix_length = 1
            if isinstance(value, Callable):
                self.define(sequence_head, value)
            elif isinstance(value, dict):
                self.load(value, sequence_head)
            for i in range(prefix_length):
                sequence_head.pop()
    

