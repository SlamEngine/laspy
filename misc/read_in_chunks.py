# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:51:06 2018

@author: gustaf.lonn
"""

import mmap
import laspy
import numpy as np

file_name='c:/test/testfile.las'
las_file = laspy.file.File(file_name)

data_provider = las_file.reader.data_provider
point_format = data_provider.pointfmt
file_number = data_provider.fileref.fileno()
header_offset = data_provider.manager.header.data_offset
point_size = data_provider.pointfmt.itemsize
file_size = data_provider.filesize()
scale = las_file.header.scale
geo_offset = las_file.header.offset
num_points = mmap.ALLOCATIONGRANULARITY*20 # this can be changed but it has to be divisible by mmap.ALLOCATIONGRANULARITY
step = num_points * point_size

hd = laspy.header.Header(point_format=las_file.header.data_format_id)
loop_idx = -1
go_on = True

while go_on:
    loop_idx += 1
    offset = header_offset//mmap.ALLOCATIONGRANULARITY+step*loop_idx
    length = point_size*num_points+header_offset
    if (offset + length > file_size):
        length = file_size - offset
        go_on = False
    memory_map = mmap.mmap(file_number,length,access = mmap.ACCESS_READ,offset=offset)
    points = np.frombuffer(memory_map, point_format, offset=header_offset)
    x = points['point']['X']*scale[0]+geo_offset[0]
    y = points['point']['Y']*scale[1]+geo_offset[1]
    z = points['point']['Z']*scale[1]+geo_offset[2]
    
    # do whatever with x, y, z...
    
    memory_map.close()

las_file.close()