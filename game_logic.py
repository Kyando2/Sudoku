from random import randint, shuffle
import time
import datetime
import multiprocessing
import logging
import json
from itertools import chain
import copy

import pyglet.shapes as shapes
import pyglet.text as text

class GameState:
    def __init__(self, matrice, me):
        self.actives = []
        self.solving = False
        self.__object_matrice = matrice
        self.magic_converter = {(int(v.x), int(v.y)): k for k, v in self.__object_matrice.items()}
        self.defaults = {}
        self.me = me
        
        # print([(cell.x, cell.y) for cell in self.board.squares[3].cells])

    def add_solved(self, num, coords):
        obj = self.__object_matrice[coords]
        label = text.Label("{0}".format(num),
                          font_name='Times New Roman',
                          font_size=36,
                          x=obj.x+obj.width/4, y=obj.y+obj.height/5,
                          )
        self.actives.append(label)
    
    def convert(self, obj):
        return self.magic_converter[(int(obj.x), int(obj.y))]

    def solve(self):
        self.board = Board(list(self.__object_matrice.keys()), self, self.defaults)
        self.solving = True
    
    def add(self, coord, num):
        self.defaults[coord] = num

    
class Region:
    def __init__(self, i):
        self.index = i
        self.__cells = []
        self.__impossibles = []

    def init_new_cell(self, cell):
        self.__cells.append(cell)
    
    @property
    def cells(self):
        return self.__cells
    
    def add_impossibles(self):
        self.__impossibles = []
        for cell in self.__cells:
            if cell.num and cell.num not in self.__impossibles:
                self.__impossibles.append(cell.num)
        for cell in self.__cells:
            cell.update_impossibles(self.__impossibles)


class Row(Region):
    pass

class Column(Region):
    pass

class Square(Region):
    pass

class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.num = None
        self.state = state
        self.is_solved = False
        self.hypothetical = 0
        self.impossibles = []
        self.possibles = []
    
    def solve(self, num):
        self.is_solved = True
        self.num = num
        self.state.add_solved(num, (self.x, self.y))
    
    def update_impossibles(self, impossibles):
        self.impossibles.extend(impossibles)

    def update_possibles(self, hypothetical=0):
        if not self.is_solved:
            self.possibles = [x for x in list(range(1, 10)) if x not in self.impossibles]
            if len(self.possibles) == 1:
                self.hypothetical = hypothetical
                # print(self.possibles, self.x, self.y)
                self.solve(self.possibles[0])
                self.is_solved = True
                self.state.board.had_change = True
        

class Board:
    def __init__(self, coords, state, default):
        default = {(0, 8): 3, (2, 7): 1, (3, 8): 2, (5, 7): 5, (5, 6): 3, (6, 7): 4, (6, 6): 9, (7, 6): 8, (8, 7): 1, (8, 8): 3, (7, 8): 6, (7, 5): 9, (5, 4): 8, (4, 4): 3, (3, 4): 5, (1, 3): 3, (1, 2): 2, (2, 2): 6, (2, 1): 3, (0, 1): 5, (0, 0): 4, (1, 0): 7, (3, 2): 3, (3, 1): 7, (5, 0): 1, (6, 2): 5, (8, 1): 8} if default == {} else default
        # default = {(0, 7): 7, (1, 7): 5, (1, 8): 3, (2, 6): 6, (3, 6): 9, (4, 6): 8, (5, 6): 4, (6, 6): 3, (4, 7): 3, (4, 8): 1, (7, 7): 4, (7, 8): 6, (8, 7): 8, (6, 5): 8, (6, 4): 6, (6, 3): 5, (7, 4): 7, (8, 4): 4, (6, 2): 2, (7, 1): 1, (8, 1): 5, (7, 0): 3, (5, 2): 5, (4, 2): 7, (3, 2): 6, (4, 1): 9, (4, 0): 4, (2, 2): 1, (1, 1): 8, (1, 0): 9, (0, 1): 6, (0, 4): 9, (1, 4): 1, (2, 4): 2, (2, 5): 3, (2, 3): 4}
        # default = {(0, 0): 4, (0, 1): 5, (0, 2): 8, (0, 4): 9, (0, 6): 2, (0, 7): 6, (0, 8): 3, (1, 0): 7, (1, 1): 1, (1, 2): 2, (1, 3): 3, (1, 4): 6, (1, 5): 5, (1, 6): 4, (1, 7): 8, (1, 8): 9, (2, 0): 9, (2, 1): 3, (2, 2): 6, (2, 6): 7, (2, 7): 1, (2, 8): 5, (3, 1): 7, (3, 2): 3, (3, 4): 5, (3, 7): 9, (3, 8): 2, (4, 2): 4, (4, 4): 3, (4, 7): 7, (5, 0): 1, (5, 2): 9, (5, 4): 8, (5, 6): 3, (5, 7): 5, (5, 8): 4, (6, 2): 5, (6, 6): 9, (6, 7): 4, (6, 8): 7, (7, 0): 3, (7, 1): 4, (7, 2): 1, (7, 3): 5, (7, 4): 7, (7, 5): 9, (7, 6): 8, (7, 7): 2, (7, 8): 6, (8, 1): 8, (8, 2): 7, (8, 6): 5, (8, 7): 1, (8, 8): 3}
        self.had_change = False
        self.items = []
        self.iteration = 0
        self.state = state
        self.rows = [Row(x) for x in range(9)]
        self.columns = [Column(x) for x in range(9)]
        self.squares = [Square(x) for x in range(9)]
        self.regions = []
        self.solved = False
        self.regions.extend(self.squares)
        self.regions.extend(self.columns)
        self.regions.extend(self.rows)
        for coord in coords:
            new_cell = Cell(coord[0], coord[1], state)
            x, y = new_cell.x, new_cell.y
            if coord in default:
                new_cell.solve(default[coord])
            self.rows[x].init_new_cell(new_cell)
            self.columns[y].init_new_cell(new_cell)
            index = 0
            for i in range(3):
                if index>9:
                    break
                for j in range(3):
                    if x <= 2+(j*3) and x >= (j*3) and y <= 2+(i*3) and y >= (i*3):
                        self.squares[index].init_new_cell(new_cell)
                        index = 200
                    index += 1
            self.items.append(new_cell)

    def solve(self, hypothetical=0):
        self.iteration += 1
        iteration = self.iteration
        if not self.solved:
            for cell in self.items:
                cell.impossibles = []
            for region in self.regions:
                region.add_impossibles()
            self.state.actives = []
            not_solved = 0
            for cell in self.items:
                cell.update_possibles(hypothetical=hypothetical)
                if cell.is_solved:
                    self.state.add_solved(cell.num, (cell.x, cell.y))
                else: not_solved+=1

            if not_solved == 0:
                self.solved = True
                if hypothetical:
                    return True


            if self.had_change == True:
                self.had_change = False
                for cell in self.items:
                    if cell.hypothetical>hypothetical:
                        cell.num = None
                        cell.is_solved = False
                        cell.hypothetical = 0
                could_solve = self.solve(hypothetical=hypothetical)
                return could_solve
            else:
                lowest = None
                for cell in self.items:
                    if not cell.is_solved:
                        if len(cell.possibles) < (len(lowest.possibles) if lowest else 9):
                            lowest = cell
                print("{1}: Hypo depth {0}, Moves to try: ".format(hypothetical, iteration), lowest.possibles)
                
                for move in lowest.possibles:

                    lowest.is_solved = True
                    lowest.hypothetical = hypothetical+1
                    lowest.num = move
                    for region in self.regions:
                        region.add_impossibles()
                    could_solve = self.solve(hypothetical=hypothetical+1)
                    if could_solve:
                        if hypothetical == 0:
                            self.solved = True
                        return True
                    else:
                        for cell in self.items:
                            if cell.hypothetical>hypothetical:
                                cell.num = None
                                cell.is_solved = False
                                cell.hypothetical = 0
                # This should never happen
                if hypothetical>0:
                    self.state.solving = False
                    return False
                '''
                elif hypothetical == 0:
                    self.state.actives = []
                    for cell in self.items:
                        
                        if cell.hypothetical>hypothetical:
                            cell.num = None
                            cell.is_solved = False
                            cell.hypothetical = 0
                        if cell.is_solved:
                            self.state.add_solved(cell.num, (cell.x, cell.y))
                    return False
                '''
                self.state.solving = False
                return False
                        # Try these
                # Do stuff if it can't be brute forced

            


            



