import cv2 
from screeninfo import get_monitors

class WindowManager():
    def __init__(self, num_doles=3) -> None:
        self.num_doles = num_doles
        self.monitors = []
        self.display_monitor_id = 0
        
        self.window_names = {
            'Mole': 'Mole', 
            'Player': 'Player', 
            'Information': 'Information'
        }
        
        self.windows_info = {
            'Mole': {
                'location': None,
                'height': None,
                'width': None,
            },

            'Player': {
                'location': None,
                'height': None,
                'width': None,
            },

            'Information': {
                'location': None,
                'height': None,
                'width': None,
            },

        }

    def get_screenInfo(self,):
        monitors = [monitor for monitor in get_monitors()]
        for m in monitors:
            monitor_info = {
                'height': m.height,
                'height_mm': m.height_mm,
                'width': m.width,
                'width_mm': m.width_mm,
                'is_primary': m.is_primary,
            }
            self.monitors.append(monitor_info)
            
        return monitors
    
    def display_monitorInfo(self,):
        for idx, x in enumerate(self.monitors):
            print(f'\n------- Monitor No.: {idx} ---------')
            print('Primary Monitor: {}'.format(x['is_primary']))
            print('Pixels:   Height    : {} \t Width     : {}'.format(x['height'], x['width']))
            print('Physical: Height(mm): {} \t Width (mm): {}'.format(x['height_mm'], x['width_mm']))

    def select_monitor(self,):
        while True:
            monitor_choice = int(input('\nSelect Monitor ID: '))
            if monitor_choice >= 0 and monitor_choice <= len(self.monitors):
                self.display_monitor_id = monitor_choice
                break
            else:
                self.display_monitorInfo()
                print(f'\nMonitor ID you selected {monitor_choice} is out of range...')
                print('Please, check --- Monitor No.: (ID number) ---')
                
    def create_windows(self, doleX_ratio=0.6, doleY_ratio=0.8):
        monitor_height = self.monitors[self.display_monitor_id]['height']
        monitor_width = self.monitors[self.display_monitor_id]['width']
        
        # Coordianate info for 'dole game' window
        dole_loc = (0, 0)
        dole_win_height = int(monitor_height * doleY_ratio)
        dole_win_width = int(monitor_width * doleX_ratio)
        self.windows_info['Mole']['location'] = dole_loc
        self.windows_info['Mole']['height'] = dole_win_height
        self.windows_info['Mole']['width'] = dole_win_width
        
        # Coordianate info for 'player' window
        player_loc = (dole_win_width, 0)
        player_win_height = dole_win_height
        player_win_width = monitor_width - dole_win_width
        self.windows_info['Player']['location'] = player_loc
        self.windows_info['Player']['height'] = player_win_height
        self.windows_info['Player']['width'] = player_win_width

        # Coordianate info for 'information' window
        info_loc = (0, dole_win_height)
        info_win_height = monitor_height - dole_win_height
        info_win_width = monitor_width
        self.windows_info['Information']['location'] = player_loc
        self.windows_info['Information']['height'] = info_win_height
        self.windows_info['Information']['width'] = info_win_width  #----------------------------------------------------------------------------------    

        # Create 'Dole Game' window
        cv2.namedWindow(self.window_names['Mole'], flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.window_names['Mole'], width=dole_win_width, height=dole_win_height)
        cv2.moveWindow(self.window_names['Mole'], x=0, y=0)

        # Create 'Player' window
        cv2.namedWindow(self.window_names['Player'], flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.window_names['Player'], width=player_win_width, height=player_win_height)
        cv2.moveWindow(self.window_names['Player'], x=player_loc[0], y=player_loc[1])

        # Create 'Information' window
        cv2.namedWindow(self.window_names['Information'], flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.window_names['Information'], width=info_win_width, height=info_win_height)
        cv2.moveWindow(self.window_names['Information'], x=info_loc[0], y=info_loc[1])

if __name__=='__main__':
    win_manager = WindowManager()
    win_manager.get_screenInfo()
    win_manager.display_monitorInfo()
    #win_manager.select_monitor()
    win_manager.create_windows()
    print('Bye, end of computation ^^')