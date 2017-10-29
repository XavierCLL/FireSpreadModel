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

    def __init__(self, ac_settings):
        print("\nSTARTING THE CELLULAR AUTOMATE\n")
        # init board properties
        self.board = Board(ac_settings["ncell_width"], ac_settings["ncell_height"],
                           ac_settings["cell_size"])
        # global time for CA
        self.time = 1

    def run(self):

        while not self.stop_condition():
            print("time step: {}".format(self.time))

            self.board.draw(self.time)
            self.next_time_step()

    def next_time_step(self):


        self.time += 1

    def stop_condition(self):
        if self.time >= 3:
            return True
        return False