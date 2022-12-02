import curses
from typing import Callable

from ast import Note

from actions import break_sequence



class Interpreter:
    """
    stores bindings in a Trie
    State machine to interpret input characters

    keys are encoded using ord(ch),
    to allow using special chars from curses"""
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
    

