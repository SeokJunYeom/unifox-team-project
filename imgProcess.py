import cv2
import numpy

def imgDecode(imgStr):
	data = numpy.fromstring(imgStr, dtype = 'unint8')
	img = cv2.imdecode(data, 1)

	return img

def imgToString(imgPath, imgName):
	img = cv2.imread(imgPath)
	imgStr = cv2.imencode('.jpg', img)[1].tostring()

	imgLen = str(len(imgStr))
	imgStr = "image" + "*" + imgName + "*" + imgLen + "*" + imgStr

	return imgStr

def imgSave(imgPath, img):
	cv2.imwrite(imgPath, img)

def imgRead(imgPath):
        return cv2.imread(imgPath)
