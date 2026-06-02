# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage


def T(dset):
    new_dset = []
    rotate = 5
    for d in dset:
        new_d = ndimage.rotate(d, rotate, reshape=False)
        new_dset.append(new_d)
    return np.array(new_dset)

# def T(dset):
#     new_dset = []
#     sigma = 1.0  # 블러 강도
#     for d in dset:
#         new_d = ndimage.gaussian_filter(d, sigma=sigma)
#         new_dset.append(new_d)
#     return np.array(new_dset)


def E(source_y, follow_y):
    result = []
    for s, f in zip(source_y, follow_y):
        if s == f:
            result.append(True)
        else:
            result.append(False)
    return result
