import cv2
import numpy as np

from PIL import ImageFont, ImageDraw, Image
from utils.Colors import ColorCode

class InformationManager():
    '''
    Display information about mole game
    '''
    def __init__(self, goal_to_complete):
        self.hit_num_to_complete = goal_to_complete
        self.current_hit_num = 0
        self.pane_move_num = 0
        self.pane_stack = []
        self.left_margin = 5
        self.right_margin = 5
        self.text_line_space = 10
        self.bg_img = cv2.imread('./imgs/bg_white.png', cv2.IMREAD_COLOR)
        self.current_pane_id = 0
       
    def append_pane_stack(self,current_pane_id):
        self.pane_stack.append(current_pane_id)

    def increase_hit_number(self,):
        self.current_hit_num += 1

    def increase_pane_movement(self,):
        self.pane_move_num += 1
    
    def check_mission_complete(self,):
        if self.current_hit_num >= self.hit_num_to_complete:
            return True
        else:
            return False
    
    def reset_game(self,):
        self.current_hit_num = 0
        self.pane_move_num = 0
        self.current_pane_id = 0
        self.pane_stack = []
       
    def display_game_info(self, window_size_height, window_size_width):

        print(window_size_height)
        frame = cv2.resize(self.bg_img, (window_size_width, window_size_height), cv2.INTER_CUBIC)
        
        # 화면을 2:1 비율로 분할
        win_width_unit = int(window_size_width/4)
        win_height_unit = int(window_size_height/3)
    
                
        # 운동량 바깥 사각형 -> 오른쪽 2칸 unit 중앙에 현재/목표수 gage 출력
        outer_rectangle_start_point = (self.left_margin, win_height_unit)
        outer_rectangle_end_point = (self.left_margin + win_width_unit*2, win_height_unit*2)
        cv2.rectangle(
            frame,
            pt1=outer_rectangle_start_point,  # 시작점 좌표(x, y)
            pt2=outer_rectangle_end_point, # 종료점 좌표(x, y)
            color=ColorCode.RED, 
            thickness=1, # 선 두께, default=1
        )
        
        # 운동량 안쪽 사각형 -> 오른쪽 2칸 unit 중앙에 현재/목표수 gage 출력
        current_count_length = int(
            (self.left_margin + win_width_unit*2) / (self.hit_num_to_complete + 1e-5) * self.current_hit_num
        )
        cv2.rectangle(                                                                               
            frame,
            pt1=outer_rectangle_start_point,  # 시작점 좌표(x, y)
            pt2=(current_count_length, win_height_unit*2), # 종료점 좌표(x, y)
            color=ColorCode.RED, 
            # color=cv2.COLORMAP_TURBO,
            thickness=-1, # 선 두께, default=1, -1일 경우 가득 채우기
        )
        
        # 왼쪽 1칸에 목표 hit, 현재 hit, pane 이동수 출력
        cv2.rectangle(
            frame,
            pt1=(self.left_margin + win_width_unit*2 + 10, 10),  # 시작점 좌표(x, y)
            pt2=(window_size_width-10, window_size_height-10), # 종료점 좌표(x, y)
            color=ColorCode.BABY_PURPLE, 
            thickness=-1, # 선 두께, default=1
        )
        #그래프 안 카운트 넘버링    (y축 win_height_unit*2하면 숫자가 박스안으로 들어감) (-10 = 상단 표시)
        cv2.putText(frame, str(int (self.current_hit_num)), (current_count_length, win_height_unit+55), cv2. FONT_HERSHEY_SCRIPT_SIMPLEX, 2, ColorCode.RED, 3) 
          
        #오른쪽 페이지 상세정보 
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        font=ImageFont.truetype('fonts/nanum/NanumBarunGothic/NanumBarunGothicBold.ttf', 30)
        draw.text( (self.left_margin + win_width_unit*2 + 20, 30), '현재 카운트 :'+ str(int (self.current_hit_num)), ColorCode.BLACK, font)
        draw.text( (self.left_margin + win_width_unit*2 + 20, 60), '목표 카운트 :'+ str(int(self.hit_num_to_complete)), ColorCode.BLACK, font)
        draw.text( (self.left_margin + win_width_unit*2 + 20, 90), '달성률 :'+ str(int(self.current_hit_num  / (self.hit_num_to_complete)*100)) + '%', ColorCode.BLACK, font)
        draw.text( (self.left_margin + win_width_unit*2 + 20, 120), 'pane 이동 횟수 :'+ str(int(len(self.pane_stack))) , ColorCode.BLACK, font)
        frame = np.array(img_pil)
        
        return frame
        

if __name__=='__main__':
    pass