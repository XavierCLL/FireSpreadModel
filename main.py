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
#            6.55
#         ___________
#        |           |
# -70.9  |           | -70.595
#        |___________|
#
#            6.355

# lat and lon:
x_min = -70.9
x_max = -70.595
y_min = 6.355
y_max = 6.55
extent = (x_min, x_max, y_min, y_max)

# cell size in decimal degrees, default: 0.001
cell_size_dd = 0.005

# start date for the fire
start_date = date(2007, 1, 2)

# define the cells on fire at start [(lon, lat), ...]
init_cells_onfire = [(-70.72449, 6.44022)]

# cell size in pixels
cell_size_p = 10


### cellular automaton settings

ca_settings = {"extent": extent, "cell_size_dd": cell_size_dd,
               "cell_size_p": cell_size_p, "start_date": start_date,
               "init_cells_onfire": init_cells_onfire}


### run

ca_spread_fires = CellularAutomaton(ca_settings)

ca_spread_fires.run()