# -*- coding: cp949 -*-

import cv2
import numpy
import sys

def imgDecode(imgStr):
	data = numpy.fromstring(imgStr, dtype = 'uint8')
	img = cv2.imdecode(data, 1)

	return img

def imgToString(img, imgName):
	imgStr = cv2.imencode('.jpg', img)[1].tostring()
	imgLen = str(len(imgStr))
	imgStr = "image" + "*" + str(imgName) + "*" + imgLen + "*" + imgStr

	return imgStr

def imgSave(imgPath, img):
	cv2.imwrite(imgPath, img)

def imgRead(imgPath):
        return cv2.imread(imgPath)
