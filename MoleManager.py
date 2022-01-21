from time import sleep
import cv2

from utils.Colors import ColorCode

class MoleManager():
    '''
    '''
    def __init__(self, bg_screen_size, divide_unit) -> None:
        self.divide_unit = divide_unit
        self.win_name = 'Mole'
        self.bg_frame =  cv2.imread('./imgs/bg_yellow.png', cv2.IMREAD_COLOR)
        self.mole_list = None
        self.mole_img = cv2.imread('./imgs/mole_jklee.jpg', cv2.IMREAD_COLOR)
        self.start_img = cv2.imread('./imgs/start_bg.png', cv2.IMREAD_COLOR)
        self.start_set_img = cv2.imread('./imgs/start_set.png', cv2.IMREAD_COLOR)
        self.mission_completed_img = cv2.imread('./imgs/bg_mission_completed.png', cv2.IMREAD_COLOR)
        self.show_up_time = 1
        self.bg_screen_size = bg_screen_size

    def create_background_image(self, win_manager):
        win_height = win_manager.windows_info[self.win_name]['height']
        win_width = win_manager.windows_info[self.win_name]['width']
        
        bg_frame = cv2.resize(self.bg_frame, (win_height, win_width), cv2.INTER_CUBIC)
        
        return bg_frame
        

    def draw_grids_on_mole_window(self, frame):
        
        frame_height, frame_width, _ = frame.shape
        # print(f'height: {frame_height}, width: {frame_width}')
        
        # Calculate unit-distance 
        unit_dist_x = frame_width / self.divide_unit
        unit_dist_y = frame_height / self.divide_unit

        # Draw Horizontal lines
        for x in range(1, self.divide_unit):
                cv2.line(
                frame, 
                (0, int(unit_dist_y * x)), 
                (frame_width, int(unit_dist_y * x)), 
                ColorCode.RED, 
            )

        # Draw vertical lines
        for x in range(1, self.divide_unit):
            cv2.line(
                frame, 
                (int(unit_dist_x * x), 0), 
                (int(unit_dist_x * x), frame_height), 
                ColorCode.RED, 
            )    
        
        return frame


if __name__=='__main__':
    # img = cv2.imread('./managers/imgs/mole.png', cv2.IMREAD_COLOR)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print()
    
    mole_manager = MoleManager()
    mole_manager.generate_grid_on_moleWindow()
    # frame = mole_manager.generate_grid_on_moleWindow()
    
    print('Bye, end of computation ^^')