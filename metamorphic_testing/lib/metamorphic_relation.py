# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage

# 반시계 방향 회전(준)
# def T(dset):
#    new_dset = []
#    rotate = 5
#    for d in dset:
#        new_d = ndimage.rotate(d, rotate, reshape=False)
#        new_dset.append(new_d)
#    return np.array(new_dset)

# 시계 방향 회전(봉)
# def T(dset):
#     new_dset = []
#     rotate = -5
#     for d in dset:
#         new_d = ndimage.rotate(d, rotate, reshape=False)
#         new_dset.append(new_d)
#     return np.array(new_dset)

# 흐림처리(준)
# def T(dset):
#     new_dset = []
#     sigma = 1.0 
#     for d in dset:
#         new_d = ndimage.gaussian_filter(d, sigma=sigma)
#         new_dset.append(new_d)
#     return np.array(new_dset)

# 흑백처리(봉)


# 선, 점추가 (준)



# 반전처리(봉)



def E(source_y, follow_y):
    result = []
    for s, f in zip(source_y, follow_y):
        if s == f:
            result.append(True)
        else:
            result.append(False)
    return result
