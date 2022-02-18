import time 
import os
import csv
import pressuresensor_mock


user_list = [1, 2]
sensor_list = []
data = []
sensors = ['Time']
period1 = input('Select a collection period, (seconds/data_point): ')
period = float(period1)

for i in range(0, len(user_list)):
    sensor_list.append(pressuresensor_mock.PressureSensor(user_list[i]))
    sensors.append('S' + str(user_list[i]))

print(sensors)
                       
runs = 0

os.chdir('/media/pi/USB20FD/DAQ_Test')
start_time = time.time()
next_time = start_time + period

while True:
    current_time = time.time()
        


    if current_time - next_time >= 0:
        
        next_time = next_time + period
        data.append(current_time-start_time)
        for i in range(0, len(sensor_list)):
            data.append(sensor_list[i].get_press())
        data_str = ['%.2f' % elem for elem in data]
        

        try:
        
            if runs == 0:
                
                with open('myFile.txt', 'w') as f:
                    
                    f.truncate()
                    csvwriter = csv.writer(f)
                    csvwriter.writerow(sensors)
                    csvwriter.writerow(data_str)

            else:
            
                with open('myFile.txt', 'a') as f:
                    csvwriter = csv.writer(f)
                    csvwriter.writerow(data_str)
                    
            print(data_str)
            
            data = []
            data_str = []
            
            runs += 1
            
                    
        except KeyboardInterrupt:
            break


    
    























    
