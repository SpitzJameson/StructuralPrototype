'''!
This program is responsible for stating which sensors are being used for a 
desired test, creating sensor object, facilitating the reading of each sensor,
and writing data to the csv file on the USB flashdrive. The program works by 
calling the get_pressure() method from the presssure_sensor class for each
specified sensor. Then it stores the sensor data in a data list and instantly
writes that list to the csv file. Then the data list is cleared and data is read
again. Additionally, this program keeps track of run time and allows the user
to specify a frequency for data collection.
'''

import time 
import os
import csv
import pressuresensor_mock

## Pressure sensor list. Can be numbers from 1 to 12.
user_list = [1, 2]
sensor_list = []

## Stores each iteration of pressure data for all sensors.
data = []

## List that is written as thr header in the csv file. Modified later.
sensors = ['Time']

## Stores period at which user wants to take data.
period1 = input('Select a collection period, (seconds/data_point): ')

## Converts specified period from string to float.
period = float(period1)

# Parses through user_list to create a list containting pressure sensor objects
# list for each sensor specified.
for i in range(0, len(user_list)):
    
    # Passes through sensor number to the sensor object so proper sensor
    # properties can be assigned
    sensor_list.append(pressuresensor_mock.PressureSensor(user_list[i]))
    sensors.append('S' + str(user_list[i]))

print(sensors)

# Counter to store how many iterations of data collection have been made.                    
runs = 0

# Changes file working directory to the USB flashdrive for data wirting to a 
# csv file within that directory.
os.chdir('/media/pi/USB20FD/DAQ_Test')

## Stores the microcontroller time at which data collection begins.
start_time = time.time()

## Variable adds period to startime to signal when the data should be read and 
#  written.
next_time = start_time + period

# Collect and write pressure and time data continuously until user terminates 
# test.
while True:
    
    ## Stores current time to reference how long data has been processed for.
    current_time = time.time()

    # Collect data if the differnce between the last and present data collections
    # is equal to the period.
    
    if current_time - next_time >= 0:
        
        next_time = next_time + period
        data.append(current_time-start_time)
        
        # Get pressure from each sensor and store in list.
        for i in range(0, len(sensor_list)):
            data.append(sensor_list[i].get_press())
            
        ## Creates string of our data for all sensors, recorded to two decimal
        #  places.
        data_str = ['%.2f' % elem for elem in data]
        

        try:
            
            # Check if this is the first run of the program.
            if runs == 0:
                
                # Open the csv file named 'myFile.txt' to write in.
                with open('myFile.txt', 'w') as f:
                    
                    # Empty the old csv file for new data collection.
                    f.truncate()
                    
                    # Writing data to file
                    csvwriter = csv.writer(f)
                    csvwriter.writerow(sensors)
                    csvwriter.writerow(data_str)

            else:
            
                # Open the csv file to write in.
                with open('myFile.txt', 'a') as f:
                    
                    # Writing data to file.
                    csvwriter = csv.writer(f)
                    csvwriter.writerow(data_str)
                    
            print(data_str)
           
            # Clear data for another iteration of data collection/writing.
            data = []
            data_str = []
            
            # Increment runs to avoid clearing the csv file again
            runs += 1
            
        # Exit loop if user pressec CTRL+C           
        except KeyboardInterrupt:
            break


    
    























    
