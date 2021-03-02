import time

import pyglet 
import pyglet.shapes as shapes
import pyglet.window.key as key

from init_mod import create_shapes
from game_logic import GameState

class GameWindow(pyglet.window.Window):
    def __init__(self, bgcolor, tilecolor):
        super(GameWindow, self).__init__()
        self.width = 700
        self.height = 600
        self.itemslist = []
        self.bgcolor = bgcolor
        self.active = None
        matrice, magic_list = create_shapes(self.itemslist ,self.width, self.height, tilecolor)
        self.ml = magic_list
        self.state = GameState(matrice, self)
        self.now = time.time()

    def on_draw(self):
        self.clear()
        background = shapes.Rectangle(x=0, y=0, width=self.width, height=self.height, color=self.bgcolor)
        background.draw()
        for item in self.ml: item.draw()
        for item in self.itemslist: item.draw()
        for item in self.state.actives: item.draw()
        if self.state.solving and time.time()-self.now>1:
            self.state.board.solve()
    
    def on_mouse_motion(self, x, y, dx, dy):
        highest_y = 0
        highest_x = 0
        possible = []
        correct = None
        for element in self.itemslist:
            if y>element.y and element.y >= highest_y:
                if element.y>highest_y:
                    possible.clear()
                possible.append(element)
                highest_y = element.y
        
        for element in possible:
            if x>element.x and element.x > highest_x:
                self.correct = element
                highest_x = element.x

    def on_key_press(self, symbol, modifiers):
        coords = tuple(self.state.convert(self.correct))
        if symbol == 65293:
            self.state.actives = []
            self.state.solve()
            return
        if 0 < symbol-48 < 10:
            self.state.add(coords, symbol-48)
            label = pyglet.text.Label("{0}".format(symbol-48),
                            font_name='Times New Roman',
                            font_size=36,
                            x=self.correct.x+self.correct.width/4, y=self.correct.y+self.correct.height/5,
                            )
            self.state.actives.append(label)
