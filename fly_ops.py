import numpy as np
import time

atk_vals = [[0], [0]]
def_1_vals = [[200], [0]]
def_2_vals = [[0], [200]]
def_3_vals = [[-200], [-200]]
def_4_vals = [[-200], [200]]
def_5_coords = [[-100], [100]]

step = 1
found1 = False
found2 = False
found3 = False
found4 = False
found5 = False

def sim_one_step():
    global step
    global found1
    global found2
    global found3
    global found4
    global found5

    # This block generates attacker coordinates. In the future, it will be modified to read from a .csv file
    if step > 50:
        atk_vals[0].append(100 - step)
    else:
        atk_vals[0].append(step)
    atk_vals[1].append(step)
    
    step = step + 1

    if not found1:
        found1 = check_catch_or_move(atk_vals, def_1_vals, 2, 1)
    if not found2:
        found2 = check_catch_or_move(atk_vals, def_2_vals, 2, 2)
    if not found3:
        found3 = check_catch_or_move(atk_vals, def_3_vals, 2, 3)
    if not found4:
        found4 = check_catch_or_move(atk_vals, def_4_vals, 2, 4)
    if not found5:
        found5 = check_catch_or_move(atk_vals, def_5_coords, 2, 5)
    
    if found1 and found2 and found3 and found4 and found5:
        time.sleep(100)

def calc_norm_dir_vector(atk_x, atk_y, def_x, def_y):
    """
    Calculates the normalized distance vector between two points in 2-dimension space

    :param atk_x: X coordinate of the attacker
    :param atk_y: Y coordinate of the attacker
    :param def_x: X coordinate of the defender
    :param def_y: Y coordinate of the defender
    """
    # Calculate direction vector
    dir_x = atk_x - def_x
    dir_y = atk_y - def_y

    # Normalize the vector
    normalizer = np.sqrt(dir_x**2 + dir_y**2)
    target_x = (dir_x / normalizer)
    target_y = (dir_y / normalizer)
    return target_x, target_y

def calc_distance(x1, y1, x2, y2):
    """
    Calculates the distance between two points in 2-dimension space

    :param x1: X coordinate of the first point
    :param y1: Y coordinate of the first point
    :param x2: X coordinate of the second point
    :param y2: Y coordinate of the second point
    """
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def move_defender(atk_vals, def_vals, velocity):
    """
    Moves the defender in the direction of the given attacker position

    :param atk_vals   : An array that holds X, Y coordinates of the attacker. Last member is current position
    :param def_vals   : An array that holds X, Y coordinates of the defender. Last member is current position
    :param velocity   : The velocity of the defender
    """
    # Get normalized direction vector from the defender to the attacker
    ndv_1_x, ndv_1_y = calc_norm_dir_vector(atk_vals[0][-1], atk_vals[1][-1], def_vals[0][-1], def_vals[1][-1])
    
    # Calculate how much X and Y coordinates should change with velocity
    move_vector_x = ndv_1_x * velocity
    move_vector_y = ndv_1_y * velocity
    
    # Update the defender's position in the array 
    def_vals[0].append(def_vals[0][-1] + move_vector_x)
    def_vals[1].append(def_vals[1][-1] + move_vector_y)

def check_catch_or_move(atk_coords, def_coords, velocity, defender_id):
    if calc_distance(atk_coords[0][-1], atk_coords[1][-1], def_coords[0][-1], def_coords[1][-1]) < 5:
        print("Defender ", defender_id, "intercepted attacker at step " , step)
        return True
    else:
        move_defender(atk_coords, def_coords, velocity)
        return False