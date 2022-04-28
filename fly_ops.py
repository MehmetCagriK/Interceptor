import numpy as np
import time
import math
import plotgen
import drones

# Use only this section to configure simulation
# Attacker configuration: Either use one of the plot generators or provide . csv file
# Hint: You can use defender's flight log as the next simulation's attacker's flight log
atk_vals_circle = plotgen.create_circle_plot(0, 0, 211, 0, 3)
# atk_vals_circle = plotgen.read_atk_flight_log('./flight_logs/defender7_fl.csv')

# Defender configuration: Create defenders with necessary parameters
def_list = [
    drones.Defender(1, 250, 250, 4, True), 
    drones.Defender(2, 100, 100, 3.7, True),
    drones.Defender(3, -200, -200, 3, True),
    drones.Defender(4, -200, 0, 3, False),
    drones.Defender(5, 0, 250, 3.7, False),
    drones.Defender(6, 0, -250, 3.7, True),
    drones.Defender(7, 300, -300, 3.7, True),
    drones.Defender(8, 0, 0, 3.7, True)]

# Simulation works like this: At every step, attacker' s position is applied
# then all the defenders follow the attacker according to their own position,
# velocity and algorithm
step = 1

def sim_one_step():
    global step
    global atk_vals

    # Attacker's only last 30 step track is drawn to reduce clutter and recognize
    # the attacker if it follows circular path better.
    atk_draw_start_index = 0
    if step > 30:
        atk_draw_start_index = step - 30
    atk_vals = [atk_vals_circle[0][atk_draw_start_index: step], atk_vals_circle[1][atk_draw_start_index: step]]
    
    step = step + 1

    # Move the defenders
    for defender in def_list:
        if not defender.intercepted:
            defender.check_catch_or_move({'X': atk_vals[0][-1], 'Y':atk_vals[1][-1]})

    return def_list
