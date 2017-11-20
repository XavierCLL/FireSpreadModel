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
from datetime import date

from cellular_automaton import CellularAutomaton

### board settings
#            ymax
#         ___________
#        |           |
#  xmin  |           | xmax
#        |___________|
#
#            ymin


###### top 21
if False:
    # lat and lon:
    x_min = -70.9
    x_max = -70.595
    y_min = 6.355
    y_max = 6.55
    extent = (x_min, x_max, y_min, y_max)

    # cell size in decimal degrees, default: 0.001
    cell_size_dd = 0.001

    # start date for the fire
    start_date = date(2007, 2, 4)

    # define the cells on fire at start [(lon, lat), ...]
    init_cells_onfire = [(-70.72449, 6.44022), (-70.722, 6.445)]  # coarse resolution

    #init_cells_onfire = [(-70.71798,6.44677), (-70.71697,6.44718)]  # fine resolution
    init_cells_onfire = [(-70.72008,6.448), (-70.71866,6.4498),
                         (-70.74029,6.423), (-70.73892,6.42472)]  # fine resolution

    # velocity of spread fire, necessary for update variables
    pixels_by_day = 1064  # pixels burned / day

###### top 12
if True:
    # lat and lon:
    x_min = -68.115
    x_max = -67.87
    y_min = 5.33
    #y_max = 5.53
    y_max = 5.49104
    extent = (x_min, x_max, y_min, y_max)

    # cell size in decimal degrees, default: 0.001
    cell_size_dd = 0.001

    # start date for the fire
    start_date = date(2007, 2, 9)

    # define the cells on fire at start [(lon, lat), ...]
    init_cells_onfire = [(-67.9695,5.46), (-67.9685,5.46)]  # fine resolution

    # velocity of spread fire, necessary for update variables
    pixels_by_day = 1936  # pixels burned / day

# cell size in pixels
cell_size_p = 10


### cellular automaton settings

ca_settings = {"extent": extent, "cell_size_dd": cell_size_dd,
               "cell_size_p": cell_size_p, "start_date": start_date,
               "init_cells_onfire": init_cells_onfire, "pixels_by_day": pixels_by_day}


### run

ca_spread_fires = CellularAutomaton(ca_settings)

ca_spread_fires.run()