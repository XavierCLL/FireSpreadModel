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

from vegetation import VegetationCover


class Cell:

    def __init__(self, size, idx_pos):
        self.state = None
        self.vegetation_cover = VegetationCover()
        self.size = size  # pixel size
        self.idx_pos = idx_pos  # (height, width)

    def get_position(self):
        pos_h = self.idx_pos[0] * self.size  # position in height
        pos_w = self.idx_pos[1] * self.size  # position in width

        return pos_h, pos_w

    def get_color(self):
        return self.idx_pos[0]*10, self.idx_pos[1]*10, 55, 255

    def next_state(self):
        pass
