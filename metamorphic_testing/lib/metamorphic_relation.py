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
# def T(dset):
#     new_dset = []
#     rotate = -9
#     for d in dset:
#         new_d = ndimage.rotate(d, rotate, reshape=False)
#         new_dset.append(new_d)
#     return np.array(new_dset)

# 흐림처리(준)
# def T(dset):
#     new_dset = []
#     sigma = 0.5 
#     for d in dset:
#         new_d = ndimage.gaussian_filter(d, sigma=sigma)
#         new_dset.append(new_d)
#     return np.array(new_dset)


# 밝기 밝게(봉)
# def T(dset):
#     new_dset = []

#     brightness = -0.05

#     for d in dset:
#         new_d = d + brightness
#         new_d = np.clip(new_d, 0.0, 1.0)
#         new_dset.append(new_d)

#     return np.array(new_dset)

# 점추가 (준)
# def add_points(img, x, y, value, size=1):
#     new_img = img.copy()
#     for i in range(-size, size + 1):
#         for j in range(-size, size + 1):
#             ny = y + i
#             nx = x + j
#             if 0 <= ny < new_img.shape[0] and 0 <= nx < new_img.shape[1]:
#                 new_img[ny, nx] = value
#     return new_img

# step = 1
# def T(dset):
#     global step
#     size = step
#     new_dset = []
#     for d in dset:
#         new_d = add_points(d, 14, 14, 1.0, size=size)
#         new_dset.append(new_d)
#     step += 1
#     return np.array(new_dset)


# 밝기 어둡게(봉)
# def T(dset):
#     new_dset = []

#     brightness = 0.05

#     for d in dset:
#         new_d = d + brightness
#         new_d = np.clip(new_d, 0.0, 1.0)
#         new_dset.append(new_d)

#     return np.array(new_dset)

# ?이진화처리
# def T(dset):
#     new_dset = []
#     threshold = 0.45

#     for d in dset:
#         new_d = np.where(d >= threshold, 1.0, 0.0)
#         new_dset.append(new_d)

#     return np.array(new_dset)

# ?반전처리
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
