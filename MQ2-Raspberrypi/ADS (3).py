
import math
import time, signal, sys 
import os
# Import the ADS1x15 module.
import Adafruit_ADS1x15

 
class ADS():

    ######################### Hardware Related Macros #########################
    ADS_PIN                       = 0        # define which analog input channel you are going to use (MCP3008)
    RL_VALUE                     = 5        # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 9.83     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
    GAIN                         = 2
    adc = Adafruit_ADS1x15.ADS1015() 

 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interal(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define how many samples you are going to take in normal operation
    READ_SAMPLE_TIMES            = 5        # define the time interal(in milisecond) between each samples in 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CO                       = 1
    GAS_SMOKE                    = 2

    def __init__(self, Ro=10, analogPin=0):
        self.Ro = Ro
        self.ADS_PIN = analogPin
       # self.adc = Adafruit_ADS1x15.ADS1015() 
        
        self.LPGCurve = [2.3,0.21,-0.47]    # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 
        self.COCurve = [2.3,0.72,-0.34]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.72), point2: (lg10000,  0.15)
        self.SmokeCurve =[2.3,0.53,-0.44]   # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.53), point2: (lg10000,  -0.22)  
                
        print("Calibrating this...")
 
        self.Ro = self.ADSCalibration(self.ADS_PIN)
        print("Calibration is done...\n")
        
        print("Ro=%f kohm" % self.Ro)
    
    
    def ADSPercentage(self):
        print("main functie:")
        val = {}
        read =self.ADSRead(0)
       # print(read)
       

        val["GAS_LPG"]  = self.ADSGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CO"]       = self.ADSGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["SMOKE"]    = self.ADSGetGasPercentage(read/self.Ro, self.GAS_SMOKE)
        return val
        
    ######################### ADSResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def ADSResistanceCalculation(self):
        print("Berekenen van sensor weerstand  deel2...\n")
        voltage = 4.096
        return float(self.RL_VALUE*(1023.0-voltage)/float(voltage));
     
     
    ######################### ADSCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          ADSResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          10, which differs slightly between different sensors.
    ############################################################################ 
    def ADSCalibration(self, ads_pin):
        val = 0.0
        voltage = 4.096
        print("Starten van calibratie clean air..\n")

        for i in range(50):          # take multiple samples

	    val += float(self.RL_VALUE*(1023.0-voltage)/float(voltage))
           # print(val)
            time.sleep(0.5)
            
        val = val/50                 # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
     
        print(val)

        return val;
      
      
    #########################  ADSRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use ADSResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def ADSRead(self, ADS_PIN):
        rs = 0.0
        print("Bereken van sensor weerstand RS...\n")
	voltage = 4.096
        for i in range(5):
            read = self.adc.read_adc(0)
            rs += float(self.RL_VALUE*(1023.0-voltage)/float(voltage))
            time.sleep(50/1000.0)

        rs = rs/5
	print(rs)

        return rs
     
    #########################  ADSGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the ADSGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def ADSGetGasPercentage(self, rs_ro_ratio, gas_id):
 #       print("Starten van calibratie deel3..\n")

        if ( gas_id == 0 ):
            return self.ADSGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == 1 ):
            return self.ADSGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == 2 ):
            return self.ADSGetPercentage(rs_ro_ratio, self.SmokeCurve)
        return 0
     
    #########################  ADSGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def ADSGetPercentage(self, rs_ro_ratio, pcurve):
#        print("Starten van calibratie deel4..\n")
        return (math.pow(10,( ((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))

