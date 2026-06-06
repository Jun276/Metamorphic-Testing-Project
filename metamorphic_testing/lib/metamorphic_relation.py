# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage

# 1. 반시계 방향 회전(준)
# def T(dset):
#    new_dset = []
#    rotate = 9
#    for d in dset:
#        new_d = ndimage.rotate(d, rotate, reshape=False)
#        new_dset.append(new_d)
#    return np.array(new_dset)

# 2. 시계 방향 회전(봉)
# def T(dset):
#     new_dset = []
#     rotate = -9
#     for d in dset:
#         new_d = ndimage.rotate(d, rotate, reshape=False)
#         new_dset.append(new_d)
#     return np.array(new_dset)

# 3. 흐림처리(준)
# def T(dset):
#     new_dset = []
#     sigma = 0.5 
#     for d in dset:
#         new_d = ndimage.gaussian_filter(d, sigma=sigma)
#         new_dset.append(new_d)
#     return np.array(new_dset)


# 4. 밝기 밝게(봉)
# def T(dset):
#     new_dset = []

#     brightness = -0.05

#     for d in dset:
#         new_d = d + brightness
#         new_d = np.clip(new_d, 0.0, 1.0)
#         new_dset.append(new_d)

#     return np.array(new_dset)

# 5. 점 개수 추가 (준)
# import random

# def add_points(img):

#     new_img = img.copy()

#     y = random.randint(0, 27)
#     x = random.randint(0, 27)

#     for dy in [-1, 0, 1]:
#         for dx in [-1, 0, 1]:

#             ny = y + dy
#             nx = x + dx

#             if 0 <= ny < 28 and 0 <= nx < 28:
#                 new_img[ny, nx, 0] = 1.0

#     return new_img

# def T(dset):

#     new_dset = []

#     for d in dset:
#         new_dset.append(add_points(d))

#     return np.array(new_dset)


# 6. 밝기 어둡게(봉)
# def T(dset):
#     new_dset = []

#     brightness = 0.05

#     for d in dset:
#         new_d = d + brightness
#         new_d = np.clip(new_d, 0.0, 1.0)
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
