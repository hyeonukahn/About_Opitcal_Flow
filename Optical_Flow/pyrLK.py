#블로그를 참고하여 작성된 코드
import numpy as np
import cv2
import time

cap = cv2.VideoCapture('./Videos/vtest.mp4')
fps = cap.get(cv2.CAP_PROP_FPS) # 프레임 수 구하기
fps = int(fps)
# 추적 경로를 그리기 위한 랜덤 색상
color = np.random.randint(0,255,(200,3))
lines = None  #추적 선을 그릴 이미지 저장 변수
prevImg = None  # 이전 프레임 저장 변수
# calcOpticalFlowPyrLK 중지 요건 설정
termcriteria =  (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)

width = int(cap.get(3))
height = int(cap.get(4))

#Video 저장을 위한 코덱 설정 및 경로 설정
fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
out = cv2.VideoWriter('./Result_Video/LK.avi', fcc, fps, (width, height))


start =time.time()

while cap.isOpened():

    ret,frame = cap.read()
    if not ret:
        break
    
    img_draw = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 처음 프레임 경우
    if prevImg is None:
        prevImg = gray
        # 추적선 그릴 이미지를 프레임 크기에 맞게 생성
        lines = np.zeros_like(frame)
        # 추적 시작을 위한 특징점 검출
        prevPt = cv2.goodFeaturesToTrack(prevImg, 200, 0.01, 10)
        cv2.imwrite('Firstscene.jpg', frame)
        
    else:
        nextImg = gray
        # 옵티컬 플로우로 다음 프레임의 특징점 찾기
        nextPt, status, err = cv2.calcOpticalFlowPyrLK(prevImg, nextImg,
                                                       prevPt, None, criteria=termcriteria)
        # 대응점이 있는 특징점, 움직인 특징점 선별
        prevMv = prevPt[status==1]
        nextMv = nextPt[status==1]
        for i,(p, n) in enumerate(zip(prevMv, nextMv)):
            px,py = p.ravel()
            nx,ny = n.ravel()
            # 이전 특징점와 새로운 특징점에 선그리기
            cv2.line(lines, (px, py), (nx,ny), color[i].tolist(), 2)
            # 새로운 특징점에 점 그리기
            cv2.circle(img_draw, (nx,ny), 2, color[i].tolist(), -1)
        # 누적된 추적 선을 출력 이미지에 합성 ---⑤
        img_draw = cv2.add(img_draw, lines)
        # 다음 프레임을 위한 프레임과 특징점 이월
        prevImg = nextImg
        prevPt = nextMv.reshape(-1,1,2)
    
    cv2.imshow('OpticalFlow-LK', img_draw)
    out.write(img_draw)
    
    if init < 2:
        init += 1
        cv2.imwrite('Secondscene.jpg', img_draw)
    
    key = cv2.waitKey(fps)
    if key == 27: # Esc:종료
        break
    elif key == 8: # Backspace:추적 이력 지우기
        prevImg = None
        
cv2.destroyAllWindows()
cap.release()
out.release()

#경과 
ex_time = time.time() - start
print(ex_time)
