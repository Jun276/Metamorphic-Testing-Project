# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage

# 반시계 방향 회전(준)
# def T(dset):
#    new_dset = []
#    rotate = 9
#    for d in dset:
#        new_d = ndimage.rotate(d, rotate, reshape=False)
#        new_dset.append(new_d)
#    return np.array(new_dset)

# 시계 방향 회전(봉)
def T(dset):
    new_dset = []
    rotate = -9
    for d in dset:
        new_d = ndimage.rotate(d, rotate, reshape=False)
        new_dset.append(new_d)
    return np.array(new_dset)

# 흐림처리(준)
# def T(dset):
#     new_dset = []
#     sigma = 1.0 
#     for d in dset:
#         new_d = ndimage.gaussian_filter(d, sigma=sigma)
#         new_dset.append(new_d)
#     return np.array(new_dset)


# 흑백처리 / 이진화처리(봉)
# def T(dset):
#     new_dset = []
#     threshold = 0.45
#     for d in dset:
#         new_d = np.where(d >= threshold, 1.0, 0.0)
#         new_dset.append(new_d)
#     return np.array(new_dset)


# 점추가 (준)
# def add_point(img, x, y, value=1.0):
#     new_img = img.copy()
#     if 0 <= y < new_img.shape[0] and 0 <= x < new_img.shape[1]:
#         new_img[y, x] = value
#     return new_img

# def T(dset):
#     new_dset = []
#     for d in dset:
#         new_d = add_point(d, 14, 14)
#         new_dset.append(new_d)
#     return np.array(new_dset)

# 반전처리(봉)
# def T(dset):
#     new_dset = []
#     for d in dset:
#         new_d = 1.0 - d
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
