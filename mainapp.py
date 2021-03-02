import logging

import pyglet
from window import GameWindow




if __name__ == "__main__":
    window = GameWindow(bgcolor=(0,0,0), tilecolor=(192,192,192))
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")


    pyglet.app.run()