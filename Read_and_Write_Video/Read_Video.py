#showing video

#import 모듈은 cv2와 pytorch만 필요합니다.
import cv2
import numpy as np

prev = None
test_video = cv2.VideoCapture("../image/vtest.mp4")
while test_video.isOpened():
    ret, frame = test_video.read()
    if ret == False:
        break
    
    img_draw = frame.copy()
    cv2.imshow('test', frame)
    
    if prev is None:
        prev = frame
    
    k = cv2.waitKey(2)
    if k == 27:
        break

test_video.release()
cv2.destroyAllWindows()