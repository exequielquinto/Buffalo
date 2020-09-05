import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import dec_to_float32

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL7::INSTR')
client = ModbusClient(method = 'rtu' , port = 'COM13' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
connection = client.connect()

rm = visa.ResourceManager()
#meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
#meter.write(':NUMERIC:FORMAT ASCII')

#FUNTIONS

#print daq.write('TEMP:NPLC?',('@101:108'))
#daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))

def measure():
    #Time
    temp['101_Time']=time.ctime()
    
    #Minutes
    temp['102_Mins']=round((time.time()-ref_time)/60)
    
    #Measure PD
    response = client.read_input_registers(5003,2,unit=1)
    PD=int(response.registers[1])
    temp['103_PD'] = PD
    
    #Measure SOC
    response = client.read_input_registers(5097,2,unit=1)
    SOC=dec_to_float32(response.registers[0], response.registers[1])
    temp['104_SOC'] = SOC
    
    #Yokogawa Power Analyzer
    meter.write(':NUMeric:HOLD ON')
    meter.write(':NUMeric:NORMal:ITEM1 P,1;ITEM2 P,2;')
    
    #Measure Pac
    Pac = float(meter.query(':NUMERIC:NORMAL:VALUE? 1'))
    temp['105_Pac'] = Pac
    
    #Measure Batt Pdc
    Pdc = float(meter.query(':NUMERIC:NORMAL:VALUE? 2'))
    temp['106_Pdc'] = Pdc
    
    #Measure Misc
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))
    time.sleep(0.5)
    temp['107_T1'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@102'))
    time.sleep(0.5)
    temp['108_T2'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@107'))
    time.sleep(0.5)
    temp['109_Ambient'] = float(daq.read())
    
    response = client.read_input_registers(5093,2,unit=1)
    Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    temp['110_Modbus_Int_Temp'] = Int_Temp
    
    #daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@113'))
    #time.sleep(0.5)
    #temp['111_Ambient_Out'] = float(daq.read())
    
    
results = pd.DataFrame()
ref_time=time.time()
temp = {}
temp['103_PD']=0
while temp['103_PD'] !=1:
                
    measured = False
    while not measured:
        try:
            print('measure')
            measure()
            measured = True
        except:
           pass 
    
    results = results.append(temp, ignore_index=True)    # 17

    #print temp['101_Time'],' ',temp['105_Pac'],'W',' ',temp['106_Pdc'],'W',temp['103_PD'],' ',temp['104_SOC'],'%'
    print temp['107_T1'],'C',temp['108_T2'],'C',temp['109_Ambient'],'C',temp['110_Modbus_Int_Temp'],'C'
    
    results.to_csv('Avel_115V_Vsense.csv')
    time.sleep(60)   # Delay in seconds before capturing results               
print('finished')