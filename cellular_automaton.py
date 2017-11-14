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
import sys
from datetime import timedelta

from board import Board

INGESTION_SCRIPTS_DIR = "/multimedia/Thesis_data/geo_data/verification/"

# add dir to python path
if INGESTION_SCRIPTS_DIR not in sys.path:
    sys.path.append(INGESTION_SCRIPTS_DIR)

from ingestion_evi import get_evi
from ingestion_ncdwppt import get_ncdwppt


class CellularAutomaton:

    def __init__(self, ca_settings):
        print("\nSTARTING THE CELLULAR AUTOMATE\n")
        # init board properties
        self.board = Board(ca_settings["extent"], ca_settings["cell_size_dd"], ca_settings["cell_size_p"])

        # init global date
        self.date = ca_settings["start_date"]
        # global step time for CA
        self.time = 1  # hours

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
        for cell in self.board.cells.values():
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
                    nb_cells[(h, w)] = self.board.get_cell(cell.idx_h + h, cell.idx_w + w)

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