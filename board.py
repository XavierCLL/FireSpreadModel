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
import dask.array as da
from dask import multiprocessing
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
        print("Init board: {}x{} cells\n".format(self.ncell_width, self.ncell_height))

        # define matrix with lon, lat center location for all pixels
        self.map_locations = OrderedDict()
        for idx_height, lat in enumerate(np.arange(round(y_min+cell_size_dd/2, 8),
                                                   round(y_max+cell_size_dd/2, 8), cell_size_dd)):
            for idx_width, lon in enumerate(np.arange(round(x_min+cell_size_dd/2, 8),
                                                      round(x_max+cell_size_dd/2, 8), cell_size_dd)):
                self.map_locations[(idx_height, idx_width)] = (lon, lat)

        self.cell_size_p = cell_size_p  # cell size in pixels
        self.cells = OrderedDict()  # dict[(idx_height, idx_width)] = cell instance

        print("  init cells and vegetation cover...")
        # create board from top-left to bottom-right and left to right
        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                self.cells[(idx_height, idx_width)] = Cell(self.cell_size_p, idx_height, idx_width,
                                                           *self.map_locations[(idx_height, idx_width)])

        # set for all cells the cover in parallel process using dask
        def func(block):
            for cell in block:
                cell.vegetation_cover.set_cover()
            return block
        stack = da.from_array(np.array(list(self.cells.values())), chunks=(100))
        cells = stack.map_blocks(func, dtype=Cell).compute(num_workers=12, get=multiprocessing.get)
        for cell in cells:
            self.cells[(cell.idx_h, cell.idx_w)] = cell

    def get_cell(self, idx_height, idx_width):
        try:
            return self.cells[(idx_height, idx_width)]
        except (IndexError, KeyError):
            # this is for the borders cells without neighbors
            return None

    def draw(self, time):

        board_height = self.ncell_height*self.cell_size_p
        board_width = self.ncell_width*self.cell_size_p
        image = Image.new("RGBA", (board_width, board_height), (255, 255, 255, 0))
        draw_square = ImageDraw.Draw(image).rectangle

        for idx_height in range(self.ncell_height):
            for idx_width in range(self.ncell_width):
                cell = self.cells[(idx_height, idx_width)]
                pos_w, pos_h = cell.get_position()
                draw_square([pos_w, pos_h, pos_w+cell.size, pos_h+cell.size],
                            fill=cell.get_color(), outline=(255, 255, 255, 255))

        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save("ca_board_t{}.png".format(time))
