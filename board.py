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
import numpy as np
from collections import OrderedDict
from PIL import Image, ImageDraw

from cell import Cell


class Board:

    def __init__(self, extent, cell_size_dd, cell_size_p):
        self.extent = extent
        x_min, x_max, y_min, y_max = extent

        # define board pixels settings
        self.ncell_width = round((x_max - x_min) / cell_size_dd)  # number of cell in the width, width pixels = width*cell_size
        self.ncell_height = round((y_max - y_min) / cell_size_dd)  # number of cell in the height, height pixels = height*cell_size
        print("Init board: {}x{}".format(self.ncell_width, self.ncell_height))

        # define matrix with lon, lat center location for all pixels
        self.map_locations = OrderedDict()
        for idx_height, lat in enumerate(np.arange(round(y_min+cell_size_dd/2, 8),
                                                   round(y_max+cell_size_dd/2, 8), cell_size_dd)[:-1]):
            for idx_width, lon in enumerate(np.arange(round(x_min+cell_size_dd/2, 8),
                                                      round(x_max+cell_size_dd/2, 8), cell_size_dd)[:-1]):
                self.map_locations[(idx_height, idx_width)] = (lon, lat)

        self.cell_size_p = cell_size_p  # cell size in pixels
        self.cells = OrderedDict()  # dict[(idx_height, idx_width)] = cell instance

        # create board from top-left to bottom-right and left to right
        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                self.cells[(idx_height, idx_width)] = Cell(self.cell_size_p, idx_height, idx_width,
                                                           *self.map_locations[(idx_height, idx_width)])

    def get_cell(self, idx_height, idx_width):
        try:
            return self.cells[(idx_height, idx_width)]
        except (IndexError, KeyError):
            # this is for the borders cells without neighbors
            return None

    def draw(self, time):

        board_height = self.ncell_height*self.cell_size_p
        board_width = self.ncell_width*self.cell_size_p
        image = Image.new("RGBA", (board_height, board_width), (255, 255, 255, 0))
        draw_square = ImageDraw.Draw(image).rectangle

        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                cell = self.cells[(idx_height, idx_width)]
                pos_h, pos_w = cell.get_position()
                draw_square([pos_h, pos_w, pos_h+cell.size, pos_w+cell.size],
                            fill=cell.get_color(), outline=(255, 255, 255, 255))

        image.save("ca_board_t{}.png".format(time))
