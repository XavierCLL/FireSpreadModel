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
import sys

INGESTION_SCRIPTS_DIR = "/multimedia/Thesis_data/geo_data/verification/"

# add dir to python path
if INGESTION_SCRIPTS_DIR not in sys.path:
    sys.path.append(INGESTION_SCRIPTS_DIR)

from ingestion_cover import get_cover

# * bosques en general (galeria y otros) => COD_COB=="3.1.*"
# * zonas pantanosas o areas humedas => COD_COB=="4.1.*"
# * herbazal denso => COD_COB=="3.2.1*"
# * pastos limpios => COD_COB=="2.3.1*"
# * arbustos o transicion => COD_COB=="3.2.*"

fire_delay = 4


def table_properties_cover(cod_cob):
    if cod_cob.startswith("3.2.1"):
        color = (222, 215, 163, 255)
        type = "Herbazal denso"
        burning_index = 0.8
        burning_time = 1.5 * fire_delay  # time steps
        return color, type, burning_index, burning_time
    if cod_cob.startswith("2.3.1"):
        color = (199, 230, 123, 255)
        type = "Pastos limpios"
        burning_index = 0.8
        burning_time = 1 * fire_delay  # time steps
        return color, type, burning_index, burning_time
    if cod_cob.startswith("3.2."):
        color = (191, 222, 144, 255)
        type = "Arbustos o zonas de transicion"
        burning_index = 0.6
        burning_time = 2 * fire_delay  # time steps
        return color, type, burning_index, burning_time
    if cod_cob.startswith("3.1"):
        color = (68, 134, 78, 255)
        type = "Bosques de galeria y otros"
        burning_index = 0.1
        burning_time = 3 * fire_delay  # time steps
        return color, type, burning_index, burning_time
    if cod_cob.startswith("4.1"):
        color = (112, 197, 198, 255)
        type = "Zonas pantanosas o areas humedas"
        burning_index = 0.1
        burning_time = 2 * fire_delay  # time steps
        return color, type, burning_index, burning_time

    color = (152, 152, 152, 255)
    type = "Otra cobertura"
    burning_index = 0.05
    burning_time = 2  # time steps
    return color, type, burning_index, burning_time


class VegetationCover:

    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat
        # index time (normal external condition) that this vegetation
        # cover necessary to burn completely
        self.burning_idx_time = None

    def set_properties(self):
        # from corin land cover ingestion script
        self.cod_cob = get_cover(self.lon, self.lat)
        # set vegetation cover properties
        self.color, self.type, self.burning_index, self.burning_time = \
            table_properties_cover(self.cod_cob)