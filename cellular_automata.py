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


class CellularAutomata:

    def __init__(self, ac_settings):
        # init board
        self.board = Board(ac_settings["ncell_width"], ac_settings["ncell_height"],
                           ac_settings["cell_size"])

    def run(self):
        print("\nSTARTING THE CELLULAR AUTOMATE\n")

        self.board.draw()
