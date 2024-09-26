import pyglet

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

pyglet.app.run()

