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
from copy import deepcopy

from vegetation import VegetationCover


class Cell:

    def __init__(self, size, idx_h, idx_w, lon, lat):
        # cell status:
        #   "unburned"
        #   "on_fire"
        #   "burned"
        self.state = "unburned"
        # used for storage the new state, change to state in the end of time step
        self.new_state = None
        # resistance to burning for this cell depends of: type cover, evi and ncdwppt
        self.resistance_to_burning = None

        # cell properties
        self.size = size  # pixel size
        self.idx_h = idx_h  # index board position in height (x)
        self.idx_w = idx_w  # index board position in width (y)
        self.lon = lon  # longitude position (x)
        self.lat = lat  # latitude position (y)
        self.vegetation_cover = VegetationCover(lon, lat)

        # external conditions
        self.evi = None  # index EVI
        self.ncdwppt = None  # number of continuous days without precipitation

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
        if self.state == "burned":
            return 0, 0, 0, 255
        elif self.state == "on_fire":
            return 255, 0, 0, 255
        else:
            return self.vegetation_cover.color

    def get_burning_time(self):
        """
        Time to take this cell burned completely, depends on:
            vegetation cover: [burning_idx_time]
            external conditions: [evi, ncdwppt, wind]
        """
        pass

    def set_resistance_to_burning(self):
        evi = deepcopy(self.evi)
        burning_index = deepcopy(self.vegetation_cover.burning_index)
        ncdwppt = deepcopy(self.ncdwppt)
        # lineal variable normalization
        # y = (x - min)/(max - min)
        evi = (evi - 0.1) / (0.4 - 0.1)
        evi = evi if evi > 0 else 0
        ncdwppt = (ncdwppt / 15.5) ** 0.5
        ncdwppt = ncdwppt if ncdwppt > 0 else 0.1
        ncdwppt = ncdwppt if ncdwppt <= 1 else 1

        self.resistance_to_burning = evi / (burning_index * ncdwppt)

    def next_state(self, nb_cells):
        fire_delay = 13.5
        # init new state no change
        new_state = deepcopy(self.state)

        ###########################
        if self.state == "unburned":
            r2b_nb_cells = 0
            for (h, w), nb_cell in nb_cells.items():
                if not nb_cell or nb_cell.state != "on_fire":
                    continue
                if abs(h) == 1 and abs(w) == 1:
                    N = 0.785  # pi/4  diagonal neighbor
                else:
                    N = 1  # adjacent neighbor
                d = 1  # spread velocity
                r2b_nb_cells += d * N

            if r2b_nb_cells != 0:
                self.resistance_to_burning -= r2b_nb_cells / (fire_delay)
                if self.resistance_to_burning <= 0:
                    new_state = "on_fire"

        ###########################
        if self.state == "on_fire":
            # TODO depends on evi and ncdwppt?
            if self.vegetation_cover.burning_time <= 1:
                new_state = "burned"
            else:
                self.vegetation_cover.burning_time -= 1

        ###########################
        if self.state == "burned":
            pass

        self.new_state = new_state




