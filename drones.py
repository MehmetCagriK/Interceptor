import math
import numpy as np
import csv

class Defender:
    """
    Defender drone class
    """
    def __init__(self, identifier, start_x, start_y, velocity, interceptor):
        """
        Constructor of a drone. Give identifier, starting position, velocity
        and intercept algorithm. interceptor = True means it will use intercept
        algorith, otherwise it will use Naive Chaser.
        """
        self.identifier = identifier
        self.cur_pos = { 'X': start_x, 'Y': start_y}
        self.pos_list = [[start_x], [start_y]]
        self.velocity = velocity
        self.interceptor = interceptor

        # In the interception mode, there are phases where Naive Chaser algorithm
        # is used. During those phases, historical data is gathered for last 10
        # steps. These variables are used to manage that history
        self.NAIVE_CHASE_MAX = 10  
        self.naive_chase_counter = 0
        self.naive_chase_angles = [0] * self.NAIVE_CHASE_MAX

        # In the interception mode, there is also compensation mode where drone
        # picks an angle and constantly watches its progress.
        self.last_angle_diff = 2 * math.pi
        self.compensated_angle = 0
        self.compensation = False
        self.intercepted = False
    
    def write_flight_log(self):
        """
        When a defender catches the attacker, defender's flight log is saved.
        Note: In future, flight logs should also saved constantly, without reducing
        performance, maybe every 100 steps. If there is no flight_logs folder
        create it.
        """
        filename = './flight_logs/defender' + str(self.identifier) + '_fl.csv'
        with open(filename, 'w', newline="") as file:
            csvwriter = csv.writer(file) # 2. create a csvwriter object
            csvwriter.writerow(['X', 'Y']) # 4. write the header
            transposed_list = np.array(self.pos_list).T.tolist()
            csvwriter.writerows(transposed_list) # 5. write the rest of the data


    def check_catch_or_move(self, atk_pos):
        """
        Entrance function to defender simulation
        """
        if math.dist([self.cur_pos['X'], self.cur_pos['Y']], [atk_pos['X'], atk_pos['Y']]) < 10:
            print("Defender ", self.identifier, "intercepted attacker at step " , len(self.pos_list[0]))
            self.write_flight_log()
            self.intercepted = True
        else:
            self.move_defender(atk_pos)
            self.intercepted = False
        
    
    def calc_norm_dir_vector(self, atk_pos):
        """
        Calculates the normalized distance vector between two points in 2-dimension space
        """
        # Calculate direction vector
        dir_x = atk_pos['X'] - self.cur_pos['X']
        dir_y = atk_pos['Y'] - self.cur_pos['Y']

        # Normalize the vector
        normalizer = math.sqrt(dir_x**2 + dir_y**2)
        target_x = (dir_x / normalizer)
        target_y = (dir_y / normalizer)
        return {'X': target_x, 'Y': target_y}
    
    def move_defender(self, atk_pos):
        """
        Moves the defender in the direction of the given attacker position. 
        There are 2 algorithms used here:
        Naive Chaser: Always follows the attacker's current position
        True Interceptor: Tries to intercept the attacker in the future. 

        :param atk_vals   : An array that holds X, Y coordinates of the attacker. Last member is current position
        :param def_vals   : An array that holds X, Y coordinates of the defender. Last member is current position
        :param velocity   : The velocity of the defender
        """

        # Get normalized direction vector from the defender to the attacker, and save it
        norm_dir_vec = self.calc_norm_dir_vector(atk_pos)
        direct_angle = norm_dir_vec

        # Interception block
        if self.interceptor:
            
            if self.naive_chase_counter == self.NAIVE_CHASE_MAX and not self.compensation:
                if np.all(np.diff(self.naive_chase_angles) != 0):
                    dist = math.dist([self.cur_pos['X'], self.cur_pos['Y']], [atk_pos['X'], atk_pos['Y']])
                    coeff = dist / 30
                    # Fix the naive angle history: When there is a transition from +pi to -pi
                    # difference checker causes giant angle changes. This block adjusts the angles
                    # so the transition doesn't cause giant angle changes.
                    for i in range(0, 9):
                        if self.naive_chase_angles[i] - self.naive_chase_angles[i + 1] < -math.pi:
                            self.naive_chase_angles[i + 1] -= 2 * math.pi
                        elif self.naive_chase_angles[i] - self.naive_chase_angles[i + 1] > math.pi:
                            self.naive_chase_angles[i + 1] += 2 * math.pi

                    self.compensated_angle = self.naive_chase_angles[9] + coeff * (self.naive_chase_angles[9] - self.naive_chase_angles[0])
                    norm_dir_vec['X'] = math.cos(self.compensated_angle)
                    norm_dir_vec['Y'] = math.sin(self.compensated_angle)
                    self.compensation = True
                    self.naive_chase_counter = 0
                    self.last_angle_diff = 2 * math.pi
            elif not self.compensation:
                self.naive_chase_angles[self.naive_chase_counter] = math.atan2(norm_dir_vec['Y'],norm_dir_vec['X'])
                self.naive_chase_counter += 1
            elif self.compensation:
                cur_angle_diff = np.arccos(np.dot([math.cos(self.compensated_angle), math.sin(self.compensated_angle)], [direct_angle['X'], direct_angle['Y']]))
                # Keep compensated flight
                if cur_angle_diff < self.last_angle_diff:
                    norm_dir_vec['X'] = math.cos(self.compensated_angle)
                    norm_dir_vec['Y'] = math.sin(self.compensated_angle)
                    self.last_angle_diff = cur_angle_diff
                else:
                    # Break compensated flight
                    self.compensation = False

        
        
        # Calculate how much X and Y coordinates should change with velocity
        move_vector_x = norm_dir_vec['X'] * self.velocity
        move_vector_y = norm_dir_vec['Y'] * self.velocity
        
        # Update the defender's position in the array
        self.cur_pos['X'] += move_vector_x
        self.cur_pos['Y'] += move_vector_y
        self.pos_list[0].append(self.cur_pos['X'])
        self.pos_list[1].append(self.cur_pos['Y'])
