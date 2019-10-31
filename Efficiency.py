import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import float32_to_msb, float32_to_lsb, pac_set, measure
import numpy as np

#Connect to Instruments
rm = visa.ResourceManager()
meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
meter.write(':NUMERIC:FORMAT ASCII')

client = ModbusClient(method = 'rtu' , port = 'COM1' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
connection = client.connect()
#print(connection)

#For load sequence
bi_time=300  #5minsBurn In time in seconds
capture_time=120   # 2mins //time in seconds for each successive eff capture
load=(3000,2700,2400,2100,2000,1800,1500,1200,1000,900,600,300,0,-3000,-2700,-2400,-2100,-2000,-1800,-1500,-1200,-1000,-900,-600,-300,0)
    
steps=np.arange(0,len(load))
print steps
print load
results = pd.DataFrame()
#ref_time=time.time()
temp = {}

for step in steps:
    
    if load[step]==3000 or load[step]==-3000:
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
    try:
        measure(temp, meter)
    except:
        try:
            print('measure error1')
            measure(temp, meter)
        except:
            print('measure error2')
            measure(temp, meter)
    
    results = results.append(temp, ignore_index=True)    # 17
    print temp['A_Time'],' ',temp['E_Pac'],'Watts',' ',temp['H_Pdc'],'Watts', temp['I_Eff'],'%',' ',temp['J_Ithd'],'%'
    results.to_csv('Efficiency.csv')

pac_set(float32_to_msb(0),float32_to_lsb(0),client)               
print('finished')