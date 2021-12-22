
def in_between(value, min, max):
    if value >= min and value < max:
        return True
    else:
        return False

def get_grid_unit_id(frame, divide_unit, loc):
    
    pos_x, pos_y = loc[0], loc[1]
    frame_height, frame_width, _ = frame.shape
    # print(f'pos_x: {pos_x} pos_y: {pos_y}')
    
    # Calculate unit-distance 
    unit_dist_x = frame_width / divide_unit
    unit_dist_y = frame_height / divide_unit
    
    unit_dist_x_list = [unit_dist_x] * divide_unit
    unit_dist_y_list = [unit_dist_y] * divide_unit
    
    # Get mole grid ID
    x_list = []
    for x, unit_x in enumerate(unit_dist_x_list):
        x_start = int(x * unit_x)
        x_end = int(x_start + unit_x )
        x_list.append((x_start, x_end))
        
    y_list = []
    for y, unit_y in enumerate(unit_dist_y_list):
        y_start = int(y * unit_y)
        # y_end = y * unit_y + unit_y 
        y_end = int(y_start + unit_y )
        y_list.append((y_start, y_end))
    
    unit_map = []
    for y_range in y_list:
        for x_range in x_list:
            unit_map.append((x_range, y_range))
    
    grid_id = None
    for idx, unit_area in enumerate(unit_map):
        x_start, x_end = unit_area[0]
        y_start, y_end = unit_area[1]
        if in_between(pos_x, x_start, x_end) and in_between(pos_y, y_start, y_end):
            grid_id = idx
            # print(f'grid_id: {grid_id} pos_x: {pos_x} pos_y: {pos_y}')
            break
        if grid_id == 0:
            print(f'grid_id: {grid_id}')
    
    if grid_id == None:
        print(f'grid_id: None, pos_x: {pos_x}, pos_y: {pos_y}')

    
    return grid_id


if __name__=='__main__':
   pass