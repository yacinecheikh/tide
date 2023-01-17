from ast import Note


# special actions

def default(app):
    "called when no shortcut exists yet"
    ch = app.state.keyboard.sequence[0]
    # can only be called when in editor state
    app.activity.ast.root.add(Note(str(ch)))


def break_sequence(app):
    "called when a sequence is cut by an undefined character"
    seq = app.activity.keyboard.sequence
    chars = []
    for ch in seq:
        if 97 <= ch <= 122:
            chars.append(chr(ch))
        else:
            chars.append(ch)
    # only applies to Editor activity
    #app.activity.ast.root.add(Note(str(chars) + ' not found'))




# camera

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


# moving in editor

def move_right(app):
    cursors = app.activity.ast.selected
    for node in cursors:
        app.state.ast.unselect(node)
        if len(node.children):
            app.activity.ast.select(node.children[0])
        else:
            app.activity.ast.select(node)


def move_left(app):
    pass

def move_up(app):
    pass

def move_down(app):
    pass


# editing
def insert_comment(app):
    editor = app.activity
    ast = editor.ast
    for node in ast.selected:
        note = Note()
        node.add(note)
        ast.unselect(node)
        ast.select(note)

