import cv2
from utils.Colors import ColorCode

def angleGage(angle, outWidth, frame):


    # 팔각도 목표 달성값 Plotting
    # 왼쪽 팔각도 게이지 그래프 출력
    # 팔의 최대 각도 160도 최소 각도 60도로 설정
    # 측정된 팔의 각도에서 최소각도를 양변에 빼주고 
    # 현재 각도에서 최소각도를 뺀 값과 최대 각도에서 
    # 최소 각도를 빼준 값을 나누면 목표 각도의 퍼센테이지 측정 가능

    jointPercent = (angle - 60) / 100

    if jointPercent < 0:
        jointPercent = 0
    else:
        jointPercent = 1

    # 막대그래프의 최대값 * 목표 각도의 퍼센테이지 = 현재 목표각도 달성 정도
    startX = 100 + (500 - round(500 * jointPercent))

    if startX < 100:
        startX = 100
    
    cv2.rectangle(
        frame, 
        pt1=(outWidth-30, 100),  # 시작점 좌표(x, y)
        pt2=(outWidth,600), # 종료점 좌표(x, y)
        color=ColorCode.RED, 
        thickness=3, # 선 두께, default=1
    )
    
    cv2.rectangle(
        frame, 
        (outWidth-30, startX), 
        (outWidth,600), 
        (0,0,255), 
        -1,
    )
    
    cv2.putText(
        frame,
        str(round(100*jointPercent)),
        (outWidth-45, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (0,0,255),
        2,
    )

    return frame
