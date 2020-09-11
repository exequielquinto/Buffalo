import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import dec_to_float32

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL7::INSTR')

#client = ModbusClient(method = 'rtu' , port = 'COM4' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
#connection = client.connect()

#rm = visa.ResourceManager()
#meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
#eter.write(':NUMERIC:FORMAT ASCII')

def measure():
    #Time
    temp['101_Time']=time.ctime()
    
    #Minutes
    #temp['102_Mins']=round((time.time()-ref_time)/60)
    temp['102_Mins']=((time.time()-ref_time)/60)
    
    #Measure PD
    #response = client.read_input_registers(5003,2,unit=1)
    #PD=int(response.registers[1])
    #temp['103_PD'] = PD
    
    #Measure SOC
    #response = client.read_input_registers(5097,2,unit=1)
    #SOC=dec_to_float32(response.registers[0], response.registers[1])
    #temp['104_SOC'] = SOC
    
    #response = client.read_input_registers(5093,2,unit=1)
    #Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    #temp['105_Modbus_Int_Temp'] = Int_Temp
    
    #response = client.read_input_registers(5053,2,unit=1)
    #Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    #temp['106_Modbus_AC_Watts_Grid'] = Int_Temp
    
    #response = client.read_input_registers(5005,2,unit=1)
    #Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    #temp['107_Modbus_Vdc'] = Int_Temp
    
    #response = client.read_input_registers(5007,2,unit=1)
    #Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    #temp['108_Modbus_Idc'] = Int_Temp
    
    #Measure Misc
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))
    time.sleep(0.5)
    temp['109_CM1_Core'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@102'))
    time.sleep(0.5)
    temp['110_CM1_Coil'] = float(daq.read())
        
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@103'))
    time.sleep(0.5)
    temp['111_T5'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@104'))
    time.sleep(0.5)
    temp['112_K3'] = float(daq.read())

    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@105'))
    time.sleep(0.5)
    temp['113_U2'] = float(daq.read())    
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@106'))
    time.sleep(0.5)
    temp['114_CT4'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@107'))
    time.sleep(0.5)
    temp['115_Main_Trf'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@108'))
    time.sleep(0.5)
    temp['116_Lab_Amb'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@109'))
    time.sleep(0.5)
    temp['116_C2'] = float(daq.read())
    
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@110'))
    time.sleep(0.5)
    temp['116_K8'] = float(daq.read())
    
results = pd.DataFrame()
ref_time=time.time()
temp = {}
#temp['103_PD']=0
#while temp['103_PD'] !=1:
while 1:
    
# measure()
    measured = False
    while not measured:
        try:
            print('measure')
            measure()
            measured = True
        except:
           pass 
    
    results = results.append(temp, ignore_index=True)    # 17
    #print temp['A_Time'],' ',temp['E_Pac_Grid'],'Watts',' ',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['I_Choke_Backplate_Temp'],'C',' ',temp['J_Choke_Core_Temp'],'C',' ',temp['K_Choke_Top_Temp'],'C',' ',temp['L_Trf_Pri_Temp'],'C',' ',temp['M_Trf_Sec_Temp'],'C'
    #print temp['A_Time'],' ',temp['E_Pac'],'W',' ',temp['F_Pdc'],'W',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['G_Q15_P2'],'C',' ',temp['H_Q16_P2'],'C',' ',temp['K_Q1_Htsk'],'C',temp['L_Ext_Amb'],'C',temp['M_Int_Temp'],'C',temp['N_U5_P2'],'C'
    #print temp['101_Time'],' ',temp['106_Modbus_AC_Watts_Grid'],'W',' ',temp['107_Modbus_Vdc'],'V',temp['108_Modbus_Idc'],'A',temp['103_PD'],' ',temp['104_SOC'],'%'
    #print temp['105_Modbus_Int_Temp'],'C',temp['116_Lab_Amb'],'C'
    print temp['116_Lab_Amb'],'C'
    print temp['109_CM1_Core'],'C',temp['110_CM1_Coil'],'C',temp['111_T5'],'C',temp['112_K3'],'C',temp['113_U2'],'C'
    print temp['114_CT4'],'C',temp['115_Main_Trf'],'C',temp['116_C2'],temp['116_K8'],'C'
    
    results.to_csv('Thermals_Pylon_Witness_Test.csv')
    time.sleep(30)   # Delay in seconds before capturing results               
print('finished')