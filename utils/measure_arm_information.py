import cv2
import numpy as np
import mediapipe as mp
import math 

from PIL import ImageFont, ImageDraw, Image
from utils.angle_calculaters import calculate_angle

mpDraw= mp.solutions.drawing_utils  #미디어 파이프 초록색 선 그리기
mpPose = mp.solutions.pose
pose = mp.solutions.pose.Pose()

def measure_shoulder_elbow_wrist_loc(frame, success_crit=30):
    results = pose.process(frame)
    try:
        landmark = results.pose_landmarks.landmark
        
        # 좌측 어깨 좌표
        LEFT_SHOULDER = (
            landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
            landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y
        )
        
        # 좌측 팔꿈치 좌표
        LEFT_ELBOW = (
            landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
            landmark[mpPose.PoseLandmark.LEFT_ELBOW].y
        )

        # 좌측 손목 좌표
        LEFT_WRIST = (
            landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
            landmark[mpPose.PoseLandmark.LEFT_WRIST].y
        )

        # 좌측 검지 좌표
        LEFT_INDEX = (
            landmark[mpPose.PoseLandmark.LEFT_INDEX].x,
            landmark[mpPose.PoseLandmark.LEFT_INDEX].y
        )

        # 우측 어깨 좌표
        RIGHT_SHOULDER = (
            landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
            landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
        )
        
        # 우측 팔꿈치 좌표
        RIGHT_ELBOW = (
            landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
            landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y
        )

        # 우측 손목 좌표
        RIGHT_WRIST = (
            landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
            landmark[mpPose.PoseLandmark.RIGHT_WRIST].y
        )
        
        # 우측 검지 좌표
        RIGHT_INDEX = (
            landmark[mpPose.PoseLandmark.RIGHT_INDEX].x,
            landmark[mpPose.PoseLandmark.RIGHT_INDEX].y
        )

        shoulder_loc = {
            'left': LEFT_SHOULDER,
            'right': RIGHT_SHOULDER,
        }
        
        elbow_loc = {
            'left': LEFT_ELBOW,
            'right': RIGHT_ELBOW,
        }
        
        wrist_loc = {
            'left': LEFT_WRIST,
            'right': RIGHT_WRIST,
        }
        
        index_loc = {
            'left': LEFT_INDEX,
            'right': RIGHT_INDEX,
        }
        
    except:
        shoulder_loc = None
        elbow_loc = None
        wrist_loc = None
        index_loc = None
        
    return shoulder_loc, elbow_loc, wrist_loc, index_loc

# 팔 각도 120도 이상 확인, 팔 거리를 계산
def measure_arm_distance(frame, win_name, success_crit=30):
    '''
    입력된 이미지로부터 좌우 팔 각도를 계산하여 win_name 윈도우에 출력
    두 팔을 30도 이내로 구부린 경우 성공으로 판단하고, 팔 거리를 측정
    
    params:
        frame: imge, videocature가 얻어낸 이미지
        win_name: str, 결과를 시현할 윈도우 이름
    
    return: tuple, (frame, success, distance, angle)
            frame: img, 랜드마크가 표시된 이미지
            success: boolean, 팔 거리 측정을 위한 사용자 팔길이 측정 성공 여부
            distance: dict (left dist, right dist), 양팔 길이 (어깨~팔꿈치 + 팔꿈치~손목)
            angle:dict, (left angle, right angle) 팔 각도
    '''
    
    # cv2.putText(
    #     frame,
    #     str("Bend your left and right arm: less than 30 degree"),
    #     (10,20),
    #     cv2.FONT_HERSHEY_SIMPLEX,
    #     0.5,
    #     (0,0,255),
    #     2,
    # )
    
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text( (10,20), "양 팔을 30도 미만으로 구부려주세요", font=ImageFont.truetype('fonts/nanum/NanumBarunGothic/NanumBarunGothicBold.ttf',20), fill=(0,0,255))
    frame = np.array(img_pil)
    
    # l1, l2 거리 계산을 위한 관절 좌표 추출
    results = pose.process(frame)   
    
    try:
        landmark = results.pose_landmarks.landmark
        
        # 우선 전달받은 이미지 위에 랜드마크 표시
        mpDraw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mpPose.POSE_CONNECTIONS
        )

        ### 거리, 각도 계산에 필요한 좌표값 추출 ###
        # Note: 좌표값은 0과 1 사이의 값을 가짐
        #   거리를 이용하여 격자를 생성할 경우
        #   WindowManager의 스크린 정보를 활용해야 함
        
        # 좌측 어깨 좌표
        LEFT_SHOULDER = (
            landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
            landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y
        )
        
        # 좌측 팔꿈치 좌표
        LEFT_ELBOW = (
            landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
            landmark[mpPose.PoseLandmark.LEFT_ELBOW].y
        )

        # 좌측 손목 좌표
        LEFT_WRIST = (
            landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
            landmark[mpPose.PoseLandmark.LEFT_WRIST].y
        )

        # 우측 어깨 좌표
        RIGHT_SHOULDER = (
            landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
            landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
        )
        
        # 우측 팔꿈치 좌표
        RIGHT_ELBOW = (
            landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
            landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y
        )

        # 우측 손목 좌표
        RIGHT_WRIST = (
            landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
            landmark[mpPose.PoseLandmark.RIGHT_WRIST].y
        )

        # Store shoulder location into a dict
        shoulder_loc = {
            'left': LEFT_SHOULDER,
            'right': RIGHT_SHOULDER,
        }

        # print(f'좌측 어깨   좌표(x, y): {LEFT_SHOULDER[0]},\t{LEFT_SHOULDER[1]}')
        # print(f'좌측 팔꿈치 좌표(x, y): {LEFT_ELBOW[0]},\t{LEFT_ELBOW[1]}')
        # print(f'좌측 손목   좌표(x, y): {LEFT_WRIST[0]},\t{LEFT_WRIST[1]}')

        # Calculate angle for each arm
        angle_left_arm = calculate_angle(LEFT_WRIST, LEFT_ELBOW, LEFT_SHOULDER)
        angle_right_arm = calculate_angle(RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER)
        angle = {
            'left': angle_left_arm, 
            'right': angle_right_arm,
        }


        # print(angle_left_arm)
        
        # 두 팔을 30도 이내로 구부렸는지 확인하여 success 판정
        if (angle['left'] < success_crit) and (angle['right'] < success_crit):
            success = True
        else:
            success = False
        
        ### Comput arm distance ###

        # Left arm distance
        distance_from_shoulder_to_elbow_left = math.sqrt(
            (LEFT_SHOULDER[0] - LEFT_ELBOW[0])**2 + (LEFT_SHOULDER[1] - LEFT_ELBOW[1])**2  
        ) 
        distance_from_elbow_to_wrist_left = math.sqrt(
            (LEFT_ELBOW[0] - LEFT_WRIST[0])**2 + (LEFT_ELBOW[1] - LEFT_WRIST[1])**2
        )
        distance_left_arm = distance_from_shoulder_to_elbow_left + distance_from_elbow_to_wrist_left

        # Right arm distance
        distance_from_shoulder_to_elbow_right = math.sqrt(
            (RIGHT_SHOULDER[0] - RIGHT_ELBOW[0])**2 + (RIGHT_SHOULDER[1] - RIGHT_ELBOW[1])**2  
        ) 
        distance_from_elbow_to_wrist_right = math.sqrt(
            (RIGHT_ELBOW[0] - RIGHT_WRIST[0])**2 + (RIGHT_ELBOW[1] - RIGHT_WRIST[1])**2
        )
        distance_right_arm = distance_from_shoulder_to_elbow_right + distance_from_elbow_to_wrist_right
        
        # Store distance info into a dict
        distance = {
            'left': distance_left_arm, 
            'right': distance_right_arm,
        }

        # Display angles
        # cv2.putText(
        #     frame,
        #     'Left arm angle:' + str(int(angle['left'])) + '   Dist: {0:2.1f}'.format(distance['left']),
        #     (10, 40),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5,
        #     (0, 0, 255),
        #     2,
        # )
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text( (10,40), '왼쪽 팔 각도:' + str(int(angle['left'])) + '   Dist: {0:2.1f}'.format(distance['left']),
        font=ImageFont.truetype('fonts/nanum/NanumBarunGothic/NanumBarunGothicBold.ttf',20), fill=(0,0,255))
        frame = np.array(img_pil)


        # cv2.putText(
        #     frame,
        #     'Right arm angle:' + str(int(angle['right'])) + '   Dist: {0:2.1f}'.format(distance['right']),
        #     (10, 60),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5,
        #     (0, 0, 255),
        #     2,
        # )
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text( (10,60), '오른 팔 각도:' + str(int(angle['right'])) + '   Dist: {0:2.1f}'.format(distance['right']),
        font=ImageFont.truetype('fonts/nanum/NanumBarunGothic/NanumBarunGothicBold.ttf',20), fill=(0,0,255))
        frame = np.array(img_pil)
        cv2.imshow(win_name, frame)

    except:
        success = False
        distance = None
        angle = None
        shoulder_loc = None
    
    return frame, success, distance, angle, shoulder_loc


def decide_mole_hit(angle, hit_crit):
    if angle >= hit_crit:
        return True
    else:
        return False