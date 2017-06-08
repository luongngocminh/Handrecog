import numpy as np
import cv2
import math






font = cv2.FONT_HERSHEY_SIMPLEX
img = cv2.imread('<YOUR HAND IMAGE>')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray,(7,7),0)

ret,thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

max_area=0

for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
cnt=contours[ci]


hull = cv2.convexHull(cnt, returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)
print defects.shape[0]
cv2.drawContours(img, contours, -1, (0,255,0), 3)
prvPoints = tuple()
minSpace = 80
firstPoint = tuple()

c = 0
numFinger = 0
if hasattr(defects, 'shape'):
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]

		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])

		


		if len(prvPoints) != 0:
			distBetweenPoints = math.hypot(far[0]-prvPoints[0],far[1]-prvPoints[1])
			distFirstPoints = math.hypot(far[0]-firstPoint[0],far[1]-firstPoint[1])
			distStartEnd = math.hypot(start[0]-end[0],start[1]-end[1])
			if distBetweenPoints > 100 and distFirstPoints > 100 and distStartEnd > 100:
				cv2.line(img, start, end, [0,255,0], 1)
				cv2.circle(img, far, 5, [0,0,255], -1)
				cv2.circle(img, end, 10, [0,255,0], -1)
				cv2.circle(img, start, 5, [255,255,0], -1)
				cv2.putText(img, str(c) , far, font , 2 ,(255, 255 , 255), 2, cv2.LINE_AA)
				c+=1
				numFinger+=1
		else:
			firstPoint = far
			c+=1
		prvPoints = far

x,y,w,h = cv2.boundingRect(cnt)
# cv2.rectangle(img,(x,y),(x+w,y+h),(0, 0, 255),2)




cv2.putText(img,str(numFinger), (10, 500), font , 4 ,(255, 255 , 255), 2, cv2.LINE_AA)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600, 600)


cv2.imshow('image',img)


cv2.waitKey(0)
cv2.destroyAllWindows()
