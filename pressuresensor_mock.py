'''!
This program takes care of assigning calibration, pin, and ADC properties
to each sensor. In our structural prototype, we allow for the selection of 
four different sensors, each having their own properties. When a user selects
a specific sensor through our LCD user interface, a pressure object is created
which has its own calibration slope and bias, ADC output pin, analog MAX/MIN
values, and determines if the sensor is connected to ADC 1 or ADC 2. This
file can get the pressure value of a sensor, attaining its analog 
value and then calculating the corresponding current and pressure values through
calibreation curves.

NOTE: ALl of these properties are constant for each sensor, meaning the physical
setup of ADC wiring must be consistent with the sensor numbering system (1-12).
'''

# Importing Widgetlords library
from widgetlords.pi_spi import *
from widgetlords import *

class PressureSensor():

    def __init__(self, sensorNUM):

        ## Configures which ADC to read from. When the input to Mod8AI() is 
        # '0' we are reading from the ACD closest to the Pi. When the input is
        # '1' we are reading from the further ADC with the alternate chip select.
        self.inputs = Mod8AI(0)
        
        if (sensorNUM == 1):
            
            ## Calibration curve slope (Analog to Pressure)
            self.cal_slope = .0709
            
            ## Calibration curve bias (Analog to Pressure)
            self.cal_bias = -56.602
            
            ## Indicates which pin sensor is connected to (A1 = 0, A2 = 1, etc.)
            self.ADC_pin = 0
            self.inputs = Mod8AI(0)
            
            ## Indicates minimum analog value read at 4mA output
            self.analog_min = 752
            
            ## Indicates maximum analog value read at 20mA output
            self.analog_max = 3706
            
        if (sensorNUM == 2):
            self.cal_slope = .0711
            self.cal_bias = -55.052
            self.ADC_pin = 1
            self.inputs = Mod8AI(1)
            self.analog_min = 747
            self.analog_max = 3687

        if (sensorNUM == 3):
            self.cal_slope = .071
            self.cal_bias = -54.6
            self.ADC_pin = 2
            self.inputs = Mod8AI(True)
            self.analog_min = 739
            self.analog_max = 3683

        if (sensorNUM == 4):
            self.cal_slope = .071
            self.cal_bias = -54.374
            self.ADC_pin = 3
            self.inputs = Mod8AI(True)
            self.analog_min = 738
            self.analog_max = 3597
            
    def get_press(self):
     
        ## Stores current analog value read from ADC at specific pin.
        analog_value = self.inputs.read_single(self.ADC_pin)
            
        ## Converts analog_value to current using experimentally calculated 
        # calibration curves.
        current = counts_to_value(analog_value, self.analog_min, self.analog_max, 4, 20)
        
        ## Converts analog_value to pressure using experimentally calculated 
        # calibration curves.
        pressure = self.cal_slope*analog_value+self.cal_bias
        
        return analog_value
       
    
    def get_pin(self):
        
        # Can return ADC pin assignment for troubleshooting.
        
        return self.ADC_pin
