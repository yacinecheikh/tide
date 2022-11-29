from ast import Note



def slide_right(app):
    app.view.move(1, 0)

def slide_left(app):
    app.view.move(-1, 0)

def slide_up(app):
    app.view.move(0, -1)

def slide_down(app):
    app.view.move(0, 1)

def quit_app(app):
    app.running = False


def default(app):
    "called when no shortcut exists yet"
    ch = app.key_interpreter.sequence[0]
    app.display.element.add(Note(ch))


def break_sequence(app, seq):
    "called when a sequence is cut by an undefined character"
    seq = app.key_interpreter.sequence
    app.display.element.add(Note(str(seq) + ' not found'))


