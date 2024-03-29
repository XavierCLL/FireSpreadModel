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
import numpy as np
import dask.array as da
from dask import multiprocessing
from datetime import timedelta

from board import Board
from cell import Cell

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
        # define the init on fires cells
        for lon, lat in ca_settings["init_cells_onfire"]:
            cell = self.board.cells[self.board.get_map_location(lon, lat)]
            cell.state = "on_fire"

        # init global date (don't change over time steps, for get current date => date + time)
        self.date = ca_settings["start_date"]
        # global step time for CA
        self.time = 1
        # for update variables
        self.pixels_by_day = ca_settings["pixels_by_day"]
        self.day_number = 1

    def run(self):

        while True:
            print("time step: {}".format(self.time))
            self.update_variables()
            self.board.draw(self.time)

            if self.stop_condition():
                break

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

    def update_variables(self):
        # get all pixels burned
        pixels_burned = len([cell for cell in self.board.cells.values() if cell.state == "burned"])
        # check if is not necessary update
        # (day1: [y n n n n], day2: [y n n n n]...)
        if pixels_burned < self.pixels_by_day * (self.day_number - 1):
            return

        print("  updating variables for the day number {}".format(self.day_number))
        current_date_time = self.date + timedelta(days=self.day_number-1)

        # set for all cells the evi in parallel process using dask
        print("    updating EVI")
        def func(block):
            for cell in block:
                cell.evi = get_evi(current_date_time, cell.lon, cell.lat)
            return block

        stack = da.from_array(np.array(list(self.board.cells.values())), chunks=(1000))
        cells = stack.map_blocks(func, dtype=Cell).compute(num_workers=8, get=multiprocessing.get)
        for cell in cells:
            # don't update evi if this is detected as burned (diff > 0.03)
            if self.board.cells[(cell.idx_h, cell.idx_w)].evi is None or \
                    not (self.board.cells[(cell.idx_h, cell.idx_w)].evi - cell.evi > 0.03):
                self.board.cells[(cell.idx_h, cell.idx_w)] = cell

        # print(self.board.cells[(20, 30)].evi)

        # set for all cells the ncdwppt in parallel process using dask
        print("    updating NCDWPPT")
        def func(block):
            for cell in block:
                cell.ncdwppt = get_ncdwppt(current_date_time, cell.lon, cell.lat)
            return block

        stack = da.from_array(np.array(list(self.board.cells.values())), chunks=(1000))
        cells = stack.map_blocks(func, dtype=Cell).compute(num_workers=8, get=multiprocessing.get)
        for cell in cells:
            self.board.cells[(cell.idx_h, cell.idx_w)] = cell

        c = self.board.cells[(30, 100)]
        print(get_ncdwppt(current_date_time, c.lon, c.lat))
        print(get_evi(current_date_time, c.lon, c.lat))
        c = self.board.cells[(150, 200)]
        print(get_ncdwppt(current_date_time, c.lon, c.lat))
        print(get_evi(current_date_time, c.lon, c.lat))

        # for cell in self.board.cells.values():
        #     cell.ncdwppt = 14 + self.day_number
        #     cell.evi = 0.27
        #     if self.time == 3 or self.time == 6:
        #         cell.ncdwppt = 1

        # update resistance_to_burning
        for cell in self.board.cells.values():
            cell.set_resistance_to_burning()

        self.day_number += 1

    def stop_condition(self):
        # if self.time > 300:  # maximum iteration
        #     return True

        # don't stop if at least one cell is on fire
        if "on_fire" not in [cell.state for cell in self.board.cells.values()]:
            return True
        else:
            return False