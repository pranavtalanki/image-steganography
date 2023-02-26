# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import mean_squared_error as compare_mse
from skimage.metrics import normalized_root_mse as compare_rmse

import imutils
import cv2
import math
# construct the argument parse and parse the arguments

imageA = cv2.imread('images/VIT.png')
imageB = cv2.imread('output.png')

imageA1=imageA.astype(float)
imageB1=imageB.astype(float)
# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(SSIM, diff) = compare_ssim(grayA, grayB, full=True)
MSE = compare_mse(imageA1, imageB1)
RMSE = compare_rmse(imageA1, imageB1)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(SSIM))
print("MSE: {}".format(MSE))
print("RMSE: {}".format(RMSE))

PSNR = 10*math.log(255**2/MSE,10)
print("PSNR: {}".format(PSNR))
# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
# show the output images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)