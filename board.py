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
from collections import OrderedDict
from PIL import Image, ImageDraw

from cell import Cell


class Board:

    def __init__(self, ncell_width, ncell_height, cell_size):
        self.ncell_width = ncell_width  # number of cell in the width, width pixels = width*cell_size
        self.ncell_height = ncell_height  # number of cell in the height, height pixels = height*cell_size
        self.cell_size = cell_size  # cell size in pixels
        self.cells = OrderedDict()  # dict[(idx_height, idx_width)] = cell instance

        # create board from top-left to bottom-right and left to right
        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                self.cells[(idx_height, idx_width)] = Cell(self.cell_size, (idx_height, idx_width))

    def get_cell(self, idx_height, idx_width):
        try:
            return self.cells[(idx_height, idx_width)]
        except IndexError:
            # this is for the borders cells without neighbors
            return None

    def draw(self, time):

        board_height = self.ncell_height*self.cell_size
        board_width = self.ncell_width*self.cell_size
        image = Image.new("RGBA", (board_height, board_width), (255, 255, 255, 0))
        draw_square = ImageDraw.Draw(image).rectangle

        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                cell = self.cells[(idx_height, idx_width)]
                pos_h, pos_w = cell.get_position()
                draw_square([pos_h, pos_w, pos_h+cell.size, pos_w+cell.size], fill=cell.get_color())

        image.save("ca_board_t{}.png".format(time))
