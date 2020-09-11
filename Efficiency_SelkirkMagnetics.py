import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import float32_to_msb, float32_to_lsb, pac_set, measure, dec_to_float32
import numpy as np

#Connect to Instruments
rm = visa.ResourceManager()
#meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
#meter.write(':NUMERIC:FORMAT ASCII')

client = ModbusClient(method = 'rtu' , port = 'COM13' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
connection = client.connect()
#print(connection)

#For load sequence
bi_time=300  #5minsBurn In time in seconds
capture_time=120   # 2mins //time in seconds for each successive eff capture

#load=(3000,2700,2400,2100,1800,1500,1200,900,600,300,0,-3000,-2700,-2400,-2100,-1800,-1500,-1200,-900,-600,-300,0)
#load=(3000,2500,2000,1500,1000,500,0,-3000,-2500,-2000,-1500,-1000,-500,0)
load=(5000,4500,4000,3500,3000,2500,2000,1500,1000,500,0,-5000,-4500,-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0)

steps=np.arange(0,len(load))
print steps
print load
#results = pd.DataFrame()
#ref_time=time.time()
temp = {}

for step in steps:
    
    if load[step]==5000 or load[step]==-5000:
        test_time=bi_time
        print step
        print ('burn in... time now is ' + time.ctime())
    else:
        test_time=capture_time
        print step
        print ('capturing... time now is ' + time.ctime())
    
    time2=time.time()
    while (time.time()-time2) < test_time:
        pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
        time.sleep(5)  # send Pac setpoint repeat
    
    print('measure')
    #measured = False
    #while not measured:
    #    try:
    #        print('measure')
    #        measure(temp, meter, client)
    #        measured = True
    #    except: 
    #       pass        
        
    #results = results.append(temp, ignore_index=True)    # 17
    #print temp['A_Time'],' ',temp['O_Int_Temp'],'C'
    #results.to_csv('Efficiency_Selkirk_New_Magnetics.csv')

#pac_set(float32_to_msb(-1000),float32_to_lsb(-1000),client)   
pac_set(float32_to_msb(0),float32_to_lsb(0),client)            
print('finished')