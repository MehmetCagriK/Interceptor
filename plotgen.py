import math
import csv
import numpy as np

# Generates a circular track and saves it to two-dimensional array
def create_circle_plot(center_x, center_y, radius, start_angle, revolution, file_to_save= None):
    circle_x = []
    circle_y = []
    for i in range(0, 360 * revolution):
        circle_x.append(center_x + math.cos(start_angle + i * (math.pi / 180)) * radius)
        circle_y.append(center_y + math.sin(start_angle + i * (math.pi / 180)) * radius)
    
    # print('Circle plot is created with 360 points')
    if isinstance(file_to_save, str):
        with open(file_to_save, 'w', newline="") as file:
            csvwriter = csv.writer(file) # 2. create a csvwriter object
            csvwriter.writerow(['X', 'Y']) # 4. write the header
            transposed_list = np.array([circle_x, circle_y]).T.tolist()
            csvwriter.writerows(transposed_list) # 5. write the rest of the data
            
    return [circle_x, circle_y]

# Writes flight logs to csv from two dimensional positional array
def write_flight_log(def_coords, filename):
    with open(filename, 'w', newline="") as file:
            csvwriter = csv.writer(file) # 2. create a csvwriter object
            csvwriter.writerow(['X', 'Y']) # 4. write the header
            csvwriter.writerows(def_coords) # 5. write the rest of the data

# Reads attacker track from the .csv file given
def read_atk_flight_log(flight_log_name):
    file = open(flight_log_name)
    csvreader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
    try:
        header = next(csvreader)
    except:
        print('Skipping header')


    rows = []
    for row in csvreader:
        rows.append(row)
    
    return np.array(rows).T.tolist()



create_circle_plot(0, 0, 300, 0, 5, 'circular.csv')
# read_atk_flight_log('circular.csv')
