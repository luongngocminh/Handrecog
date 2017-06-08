import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while(True):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	blur = cv2.blur(gray, (50,50))
	ret,thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_OTSU)
	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) != 0 : 
		cnt = contours[0]
	hull = cv2.convexHull(cnt, returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	cv2.drawContours(frame, contours, -1, (0,255,0), 3)
	prvPoints = tuple()
	minSpace = 80
	firstPoint = tuple()

	c = 1
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
					cv2.line(frame, start, end, [0,255,0], 2)
					cv2.circle(frame, far, 5, [0,0,255], -1)
					cv2.circle(frame, end, 10, [0,255,0], -1)
					cv2.putText(frame, str(c) , far, font , 2 ,(255, 255 , 255), 2, cv2.LINE_AA)
					c+=1
					numFinger+=1
			else:
				cv2.line(frame, start, end, [0,255,0], 2)
				cv2.circle(frame, far, 5, [0,0,255], -1)
				cv2.putText(frame, str(c) , far, font , 2 ,(255, 255 , 255), 2, cv2.LINE_AA)
				firstPoint = far
				c+=1
			prvPoints = far

	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0, 0, 255),2)


	cv2.putText(frame,str(numFinger), (10, 500), font , 4 ,(255, 255 , 255), 2, cv2.LINE_AA)
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()