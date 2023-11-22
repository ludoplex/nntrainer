#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2020 Jijoong Moon <jijoong.moon@samsung.com>
#
# @file	  dataset.py
# @date	  15 July 2020
# @brief  This is for mnist input generation
# @see    https://github.com/nnstreamer/nntrainer
# @author Jijoong Moon <jijoong.moon@samsung.com>
# @bug    No known bugs except for NYI items
#
#

import struct
import os
import numpy as np

TOTAL_TRAIN_DATA_SIZE=100
TOTAL_LABEL_SIZE=100
TOTAL_VAL_DATA_SIZE=20
FEATURE_SIZE = 3072

def get_data_info(target):
    t_data_size = TOTAL_TRAIN_DATA_SIZE
    v_data_size = TOTAL_VAL_DATA_SIZE
    return t_data_size, v_data_size, TOTAL_LABEL_SIZE, FEATURE_SIZE

##
# @brief load input data from file
# @return (InputVector, InputLabel, Validation Vector, ValidationLabel)
def load_data(target):
    # data_size = TOTAL_TRAIN_DATA_SIZE;
    d_size = get_data_info(target)

    if target == "validation":
        t_buf_size = d_size[0]
        v_buf_size = d_size[1]
    else:
        t_buf_size = d_size[0]*TOTAL_LABEL_SIZE
        v_buf_size = d_size[1]*TOTAL_LABEL_SIZE

    InputVector = np.zeros((t_buf_size, FEATURE_SIZE),dtype=np.float32)
    InputLabel = np.zeros((t_buf_size, TOTAL_LABEL_SIZE),dtype=np.float32)

    ValVector = np.zeros((v_buf_size,FEATURE_SIZE),dtype=np.float32)
    ValLabel = np.zeros((v_buf_size, TOTAL_LABEL_SIZE),dtype=np.float32)

    with open('vgg_valSet.dat','rb') as fin:
        for i in range(v_buf_size):
            for j in range(FEATURE_SIZE):
                data_str = fin.read(4)
                ValVector[i,j] = struct.unpack('f',data_str)[0]
            for j in range(TOTAL_LABEL_SIZE):
                data_str = fin.read(4)
                ValLabel[i,j] = struct.unpack('f',data_str)[0]
    with open('vgg_trainingSet.dat','rb') as fin:
        for i in range(t_buf_size):
            for j in range(FEATURE_SIZE):
                data_str = fin.read(4)
                InputVector[i,j] = struct.unpack('f',data_str)[0]
            for j in range(TOTAL_LABEL_SIZE):
                data_str = fin.read(4)
                InputLabel[i,j] = struct.unpack('f',data_str)[0]
    return InputVector, InputLabel, ValVector, ValLabel
