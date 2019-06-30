import numpy as np
import cv2
import math

image_path = str(r'<<provide image path>>')
exp = cv2.imread(image_path)
gray = cv2.imread(image_path, 0)

height = exp.shape[0]
width = exp.shape[1]
mask = np.zeros((height,width), np.uint8)

gray_blur = cv2.medianBlur(gray, 13)
gray_lap = cv2.Laplacian(gray_blur, cv2.CV_8UC1, ksize=5)
circles = cv2.HoughCircles(gray_lap, cv2.HOUGH_GRADIENT, 1, 180, param1=50,param2=30, minRadius=90, maxRadius=120)
print(circles)
num = len(circles[0,:])

def draw_circles(img, circles):
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in circles[0,:]:
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    return cimg

cimg = draw_circles(gray, circles)

for i, j in zip(circles[0,:], range(num)): 
    cv2.circle(mask,(i[0],i[1]),i[2],(255,255,255),thickness=-3)
    masked_data = cv2.bitwise_and(exp, exp, mask=mask)
    x = i[0] - i[2]
    y = i[1] - i[2]
    x = math.ceil(x)
    y = math.ceil(y)
    w = math.ceil(i[2]*2)
    h = math.ceil(i[2]*2)
    crop = masked_data[y:y+h,x:x+w]
    print(x,y,w,h)
    s = 256 
    k = abs(s - h)
    l = abs(s - w)
    a = np.zeros((s ,s ,3), np.uint8)
    a = np.pad(crop, ((0, k), (0, l), (0, 0)), 'constant')
    print(a.shape)
    cv2.imwrite(r'<<path for cropped images' + str(j) + r'.png', a)

cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()