# -*- coding: utf-8 -*-
import cv2
import numpy as np

def colorChange(img, value):
    color = 0
    
    for num in value:
        for x in img:
            for y in x:
                if num > 0:
                    if y[color] + num > 255:
                        y[color] = 255

                    else:
                        y[color] += num
                    
                else:
                    if y[color] + num < 0:
                        y[color] = 0

                    else:
                        y[color] += num

        color += 1

    return img

def edge(img):
    return cv2.Canny(img, 100, 200)
