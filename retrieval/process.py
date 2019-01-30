import cv2
import numpy as np


def to_sketch(src):
    g = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    i = cv2.bitwise_not(g)
    b = cv2.GaussianBlur(i, (21, 21), 0) + 1
    t = cv2.convertScaleAbs(255 * (b / (255.0001 - g)))
    m = cv2.medianBlur(t, 3)
    ret, dst = cv2.threshold(m, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    dst = remove_dots(dst)
    return dst


def remove_dots(src):
    kernal_size = 7
    (r, c) = src.shape
    img = cv2.copyMakeBorder(src, kernal_size/2, kernal_size/2, kernal_size/2, kernal_size/2, cv2.BORDER_CONSTANT, value=255)
    for x in range(kernal_size/2, kernal_size/2 + r):
        for y in range(kernal_size/2, kernal_size/2 + c):
            if img[x, y] == 255:
                continue
            is_connected = False
            for px in img[x-kernal_size/2, y-kernal_size/2:y+kernal_size/2+1]:
                if px == 0:
                    is_connected = True
                    break
            if is_connected:
                continue
            for px in img[x+kernal_size/2, y-kernal_size/2:y+kernal_size/2+1]:
                if px == 0:
                    is_connected = True
                    break
            if is_connected:
                continue
            for px in img[x-kernal_size/2+1:x+kernal_size/2, y-kernal_size/2]:
                if px == 0:
                    is_connected = True
                    break
            if is_connected:
                continue
            for px in img[x-kernal_size/2+1:x+kernal_size/2, y+kernal_size/2]:
                if px == 0:
                    is_connected = True
                    break
            if is_connected:
                continue
            for i in range(-kernal_size, 1):
                for j in range(-kernal_size, 1):
                    if 0 <= x+i < r and 0 <= y + j < c:
                        src[x+i, y+j] = 255
    return src