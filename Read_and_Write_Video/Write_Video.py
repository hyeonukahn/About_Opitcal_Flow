#saving vidoeo
import numpy as np
import cv2

def writeVideo():
    cap = cv2.VideoCapture('../image/vtest1.mp4')
    fps = 30
    width = int(cap.get(3))
    height = int(cap.get(4))
    fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = cv2.VideoWriter('../image/DIVX.avi', fcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if ret == False: break
        cv2.imshow('divx', frame)
        out.write(frame)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()

writeVideo()