
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import fly_ops



def animate(i):
    fly_ops.sim_one_step()

    # Clear the drawn plot
    plt.cla()

    # Fix the plot limits or 2d map
    plt.xlim(-300 , 300)
    plt.ylim(-300 , 300)

    # Draw tracks for attacker and defenders
    plt.plot(fly_ops.atk_vals[0], fly_ops.atk_vals[1], label='Attacker')
    plt.plot(fly_ops.def_1_vals[0], fly_ops.def_1_vals[1], label='Defender 1')
    plt.plot(fly_ops.def_2_vals[0], fly_ops.def_2_vals[1], label='Defender 2')
    plt.plot(fly_ops.def_3_vals[0], fly_ops.def_3_vals[1], label='Defender 3')
    plt.plot(fly_ops.def_4_vals[0], fly_ops.def_4_vals[1], label='Defender 4')
    plt.plot(fly_ops.def_5_coords[0], fly_ops.def_5_coords[1], label='Defender 5')

plt.style.use('fivethirtyeight')
plt.gcf().set_size_inches((8, 8))
matplotlib.rcParams['lines.linewidth'] = 2 
ani = FuncAnimation(plt.gcf(), animate, interval=5)
plt.show()