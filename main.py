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

from cellular_automaton import CellularAutomaton

### automate cellular settings

ac_settings = {"ncell_width": 20, "ncell_height": 20, "cell_size": 150}

### run

ac_spread_fires = CellularAutomaton(ac_settings)

ac_spread_fires.run()