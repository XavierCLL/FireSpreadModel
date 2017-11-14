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

    def __init__(self, size, idx_h, idx_w, lon, lat):
        # cell status
        # 0=burned, 1=unburned, 2=on_fire
        self.state = {"burned": False, "unburned": True, "on_fire": False}
        self.new_state = None  # used for storage the new state, change to state in the end

        # cell properties
        self.size = size  # pixel size
        self.idx_h = idx_h  # index board position in height (x)
        self.idx_w = idx_w  # index board position in width (y)
        self.lon = lon  # longitude position (x)
        self.lat = lat  # latitude position (y)
        self.vegetation_cover = VegetationCover(lon, lat)

        # external conditions
        self.evi = None  # index EVI
        self.ndwppt = None  # number of days without precipitation

    def get_position(self):
        """
        Get pixel position inside board (based on index board position)
        """
        pos_w = self.idx_w * self.size  # position in width
        pos_h = self.idx_h * self.size  # position in height

        return pos_w, pos_h

    def get_color(self):
        """
        Return (R, G, B, A) for draw this cell
        """
        if self.state["burned"]:
            return 0, 0, 0, 255
        elif self.state["on_fire"]:
            return 255, 0, 0, 255
        else:
            return self.vegetation_cover.color

    def get_burning_time(self):
        """
        Time to take this cell burned completely, depends on:
            vegetation cover: [burning_idx_time]
            external conditions: [evi, ndwppt, wind]
        """
        pass

    def next_state(self, nb_cells):
        #new_state = {}
        new_state = self.state


        self.new_state = new_state