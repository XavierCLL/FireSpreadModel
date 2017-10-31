#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2017 Xavier Corredor Llano
#  Email: xcorredorl <a> unal.edu.co
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#

from board import Board


class CellularAutomaton:

    def __init__(self, ca_settings):
        print("\nSTARTING THE CELLULAR AUTOMATE\n")
        # init board properties
        self.board = Board(ca_settings["ncell_width"], ca_settings["ncell_height"],
                           ca_settings["cell_size"])
        # global time for CA
        self.time = 1

    def run(self):

        while not self.stop_condition():
            print("time step: {}".format(self.time))

            self.board.draw(self.time)
            self.next_time_step()

    def next_time_step(self):
        """
        Go to the next time step, applying the transition function
        to all cells in the board
        """
        for (idx_h, idx_w), cell in self.board.cells.items():
            # get all neighbor cells for this cell
            #
            #   | (-1,-1)| (-1,0)| (-1,1)|
            #   | (0,-1) | (0,0) | (0,1) |
            #   | (1,-1) | (1,0) | (1,1) |
            #
            nb_cells = {}
            for h in [-1, 0, 1]:
                for w in [-1, 0, 1]:
                    if h == 0 and w == 0: continue
                    nb_cells[(h, w)] = self.board.get_cell(cell.idx_pos[0]+h, cell.idx_pos[1]+w)

            # go to the next stage
            cell.next_state(nb_cells)

        # now set the new state to real state of cells, this is
        # for no change state of cell while are applying the
        # transition functions
        for cell in self.board.cells.values():
            cell.state = cell.new_state
        # next time
        self.time += 1

    def stop_condition(self):
        if self.time >= 3:
            return True
        return False