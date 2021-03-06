import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import float32_to_msb, float32_to_lsb, pac_set,  dec_to_float32, Active_Sleep
import numpy as np

#Connect to Instruments
rm = visa.ResourceManager()
#daq = rm.open_resource('ASRL7::INSTR')
scope = rm.open_resource('USB0::0x0699::0x0455::C011137::0::INSTR')

client = ModbusClient(method = 'rtu' , port = 'COM5' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
connection = client.connect()

#meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
#eter.write(':NUMERIC:FORMAT ASCII')

def measure():
    #Time
    temp['101_Time']=time.ctime()
    
    #Minutes
    #temp['102_Mins']=round((time.time()-ref_time)/60)
    temp['102_Mins']=((time.time()-ref_time)/60)
    
    #Measure State
    response = client.read_input_registers(4999,2,unit=1)
    State=int(response.registers[1])
    temp['103_State'] = State
    
    #Measure Permissive
    response = client.read_input_registers(5001,2,unit=1)
    Permissive = int(response.registers[1])
    temp['104_Permissive'] = Permissive
    
    #Measure Permissive_Data
    response = client.read_input_registers(5003,2,unit=1)
    Permissive_Data = int(response.registers[1])
    temp['105_Permissive_Data'] = Permissive_Data
    
    #Measure Inverter AC Voltage
    response = client.read_input_registers(5013,2,unit=1)
    Inv_AC_Voltage = dec_to_float32(response.registers[0], response.registers[1])
    temp['106_Inv_AC_Voltage'] = Inv_AC_Voltage
    
    #Measure Iac_Internal
    response = client.read_input_registers(5089,2,unit=1)
    Iac_Internal = dec_to_float32(response.registers[0], response.registers[1])
    temp['107_Iac_Internal'] = Iac_Internal
    
    #Measure Watts_Inverter
    response = client.read_input_registers(5035,2,unit=1)
    Watts_Inverter = dec_to_float32(response.registers[0], response.registers[1])
    temp['108_Watts_Inverter'] = Watts_Inverter
    
    #Measure Vac_Grid_L2L
    response = client.read_input_registers(5015,2,unit=1)
    Vac_Grid_L2L = dec_to_float32(response.registers[0], response.registers[1])
    temp['109_Vac_Grid_L2L'] = Vac_Grid_L2L
    
    #Measure Iac_External
    response = client.read_input_registers(5021,2,unit=1)
    Iac_External = dec_to_float32(response.registers[0], response.registers[1])
    temp['110_Iac_Internal'] = Iac_External
    
    #Measure AC_Watts_Grid
    response = client.read_input_registers(5053,2,unit=1)
    AC_Watts_Grid = dec_to_float32(response.registers[0], response.registers[1])
    temp['111_AC_Watts_Grid'] = AC_Watts_Grid
    
    #Measure Freq_Grid
    response = client.read_input_registers(5009,2,unit=1)
    Freq_Grid = dec_to_float32(response.registers[0], response.registers[1])
    temp['112_Freq_Grid'] = Freq_Grid
    
    #Measure Freq_Master
    response = client.read_input_registers(5011,2,unit=1)
    Freq_Master = dec_to_float32(response.registers[0], response.registers[1])
    temp['113_Freq_Master'] = Freq_Master
    
    #Measure Int_Vdc
    response = client.read_input_registers(5005,2,unit=1)
    Int_Vdc = dec_to_float32(response.registers[0], response.registers[1])
    temp['114_Int_Vdc'] = Int_Vdc
    
    #Measure Idc
    response = client.read_input_registers(5007,2,unit=1)
    Idc = dec_to_float32(response.registers[0], response.registers[1])
    temp['115_Idc'] = Idc
    
    #Measure Battery_Vdc
    response = client.read_input_registers(5103,2,unit=1)
    Battery_Vdc = dec_to_float32(response.registers[0], response.registers[1])
    temp['116_Battery_Vdc'] = Battery_Vdc
    
    #Measure Battery_Idc
    response = client.read_input_registers(5105,2,unit=1)
    Battery_Idc = dec_to_float32(response.registers[0], response.registers[1])
    temp['117_Battery_Idc'] = Battery_Idc
    
    #Measure SOC
    response = client.read_input_registers(5097,2,unit=1)
    SOC=dec_to_float32(response.registers[0], response.registers[1])
    temp['118_SOC'] = SOC
    
    #Measure Internal_Temp
    response = client.read_input_registers(5093,2,unit=1)
    Internal_Temp=dec_to_float32(response.registers[0], response.registers[1])
    temp['119_Internal_Temp'] = Internal_Temp
    
    #Measure Fault_Code
    response = client.read_input_registers(5999,2,unit=1)
    Fault_Code = int(response.registers[1])
    temp['120_Fault_Code'] = Fault_Code
    
    #Measure Permissive_Code
    response = client.read_input_registers(6001,2,unit=1)
    Permissive_Code = int(response.registers[1])
    temp['121_Permissive_Code'] = Permissive_Code
    
    #Measure Timestamp   Wrong reading
    #response = client.read_input_registers(6003,2,unit=1)
    #Timestamp = int(response.registers[1])
    #temp['122_Timestamp'] = Timestamp

load=(3000,2500,2000,1500,1000,500,-3000,-2500,-2000,-1500,-1000,-500)
steps=np.arange(0,len(load))
print steps
print load
        
results = pd.DataFrame()
ref_time=time.time()
temp = {}
temp['103_State']=5
temp['118_SOC']=50
ctr=0
Prev_Vac=230
angle=70
unit=3
v_step=15
scope.write('ACQ:STATE ON')
time.sleep(20)
#while temp['103_State'] !=10:
    
for step in steps:
    stp_ctr=0
    while stp_ctr<10:  
        #if temp['103_State']==5:# and temp['118_SOC']>90:# or temp['103_State']!=3:
            #Pac=-Pac
            #time.sleep(2)
        #print step
        #pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
        #pac_set(float32_to_msb(Pac),float32_to_lsb(Pac),client)
                
        #measure()
        measured = False
        while not measured:
            try:
                #print('measure')
                measure()
                measured = True
            except:
                pass      
        
        pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
            
        if (temp['109_Vac_Grid_L2L']-Prev_Vac)>3:
            stp_ctr=stp_ctr+1
            print stp_ctr
            
        Prev_Vac=temp['109_Vac_Grid_L2L']
                  
        if temp['103_State']==4 or temp['103_State']==3:
            ctr=0
    
        else:
            if temp['103_State']==5 and ctr==3:
                Active_Sleep(1,client)
                time.sleep(1)
                Active_Sleep(0,client)
                time.sleep(1)
                ctr=0
            else:
                ctr=ctr+1
                
        results = results.append(temp, ignore_index=True)    # 17
        print temp['103_State'], temp['105_Permissive_Data'],temp['104_Permissive'], temp['121_Permissive_Code'], temp['120_Fault_Code'], temp['108_Watts_Inverter'], temp['109_Vac_Grid_L2L'], temp['118_SOC']
        results.to_csv('Vac_Step_85_400_10_'+'Unit'+str(unit)+'_'+str(v_step)+'_'+str(angle)+'.csv') 
        #time.sleep(1)
    print('finished1')
scope.write('ACQ:STATE OFF')
time.sleep(20)
scope.write('SAVE:IMAG:FILEF PNG')
scope.write('HARDCOPY START')
raw_data = scope.read_raw()
fid = open('Unit'+str(unit)+'_'+str(v_step)+'_'+str(angle)+'.png','wb')
fid.write(raw_data)
fid.close()
               
print('finished')
time.sleep(500)
pac_set(float32_to_msb(-1500),float32_to_lsb(-1500),client)