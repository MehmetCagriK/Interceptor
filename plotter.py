import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import fly_ops



def animate(i):
    def_list = fly_ops.sim_one_step()

    # Clear the drawn plot
    plt.cla()

    # Set the plot limits or 2d map. This has to be called repetitively because
    # FuncAnimation resets these settings.
    plt.xlim(-300 , 300)
    plt.ylim(-300 , 300)
    
    plt.plot(fly_ops.atk_vals[0], fly_ops.atk_vals[1], label='Attacker')
    for defender in def_list:
        plt.plot(defender.pos_list[0], defender.pos_list[1])

plt.style.use('fivethirtyeight')
plt.gcf().set_size_inches((8, 8)) # Set the opened window size for figure.
matplotlib.rcParams['lines.linewidth'] = 2 
ani = FuncAnimation(plt.gcf(), animate, interval=20)
plt.show()