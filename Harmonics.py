import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import float32_to_msb, float32_to_lsb, pac_set, measure, harmonics
import numpy as np

#Connect to Instruments
rm = visa.ResourceManager()
meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
meter.write(':NUMERIC:FORMAT ASCII')

client = ModbusClient(method = 'rtu' , port = 'COM14' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
connection = client.connect()
#print(connection)

#For load sequence
bi_time=120  #5minsBurn In time in seconds
#bi_time=900   #For Aux separated test, fans always full blast
capture_time=120   # 2mins //time in seconds for each successive eff capture
load=(3000,2000,1000,-3000,-2000,-1000)
    
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
        harmonics(temp, meter)
    except:
        try:
            print('measure error1')
            harmonics(temp, meter)
        except:
            print('measure error2')
            harmonics(temp, meter)
    
    results = results.append(temp, ignore_index=True)    # 17
    #print temp['A_Time'],' ',temp['F_Pac'],'Watts',' ',temp['I_Pdc'],'Watts', temp['J_Eff'],'%',' ',temp['K_Ithd'],'%'
    results.to_csv('Harmonics_Unit2_3FEt.csv')

pac_set(float32_to_msb(0),float32_to_lsb(0),client)               
print('finished')