import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from Functions import dec_to_float32

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL13::INSTR')
client = ModbusClient(method = 'rtu' , port = 'COM1' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
connection = client.connect()

rm = visa.ResourceManager()
meter = rm.open_resource('USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
meter.write(':NUMERIC:FORMAT ASCII')

#FUNTIONS

#print daq.write('TEMP:NPLC?',('@101:108'))
#daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))

def measure():
    #Time
    temp['A_Time']=time.ctime()
    
    #Minutes
    temp['B_Mins']=round((time.time()-ref_time)/60)
    
    #Measure PD
    response = client.read_input_registers(5003,2,unit=1)
    #print response.registers[0]
    #print response.registers[1]
    PD=int(response.registers[1])
    temp['C_PD'] = PD
    
    #Measure SOC
    response = client.read_input_registers(5097,2,unit=1)
    SOC=dec_to_float32(response.registers[0], response.registers[1])
    temp['D_SOC'] = SOC
    
    #Yokogawa Power Analyzer
    meter.write(':NUMeric:HOLD ON')
    meter.write(':NUMeric:NORMal:ITEM1 P,1;ITEM P,2;')
    
    #Measure Pac
    Pac = float(meter.query(':NUMERIC:NORMAL:VALUE? 3'))
    temp['E_Pac'] = Pac
    
    #Measure Batt Pdc
    Pdc = float(meter.query(':NUMERIC:NORMAL:VALUE? 6'))
    temp['F_Pdc'] = Pdc
    
    #Measure Q15_P2
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))
    time.sleep(0.5)
    temp['G_Q15_P2'] = float(daq.read())
    
    #Measure Q16_P2
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@301'))
    time.sleep(0.5)
    temp['H_Q16_P2'] = float(daq.read())
    
    #Measure Q2_P1
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@102'))
    time.sleep(0.5)
    temp['I_Q2_P1'] = float(daq.read())
    
    #Measure Q1_P1
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@303'))
    time.sleep(0.5)
    temp['J_Q1_P1'] = float(daq.read())
    
    #Measure Q15_P2 Htsk 
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@304'))
    time.sleep(0.5)
    temp['K_Q1_Htsk'] = float(daq.read())
    
    #Measure Ext Amo
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@305'))
    time.sleep(0.5)
    temp['L_Ext_Amb'] = float(daq.read())
       
    #Measure Internal Temp
    response = client.read_input_registers(5093,2,unit=1)
    Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    temp['M_Int_Temp'] = Int_Temp

    
results = pd.DataFrame()
ref_time=time.time()
temp = {}
temp['C_PD']=0
while temp['C_PD'] !=1:
    
    #measure()
    try:
        measure()       
    except:
        try:
            print('measure error1')
            time.sleep(1)
            measure()
        except:
            try:
                print('measure error2')
                time.sleep(1)
                measure()
            except:
                print('measure error3')
                time.sleep(1)
                measure()
    
    results = results.append(temp, ignore_index=True)    # 17
    #print temp['A_Time'],' ',temp['E_Pac_Grid'],'Watts',' ',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['I_Choke_Backplate_Temp'],'C',' ',temp['J_Choke_Core_Temp'],'C',' ',temp['K_Choke_Top_Temp'],'C',' ',temp['L_Trf_Pri_Temp'],'C',' ',temp['M_Trf_Sec_Temp'],'C'
    print temp['A_Time'],' ',temp['E_Pac_Grid'],'Watts',' ',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['J_Choke_Core_Temp'],'C',' ',temp['L_Choke_Core_Top_Temp'],'C',' ',temp['M_Choke_Top_Temp'],'C',temp['N_Trf_Pri_Temp'],'C',temp['O_Trf_Sec_Temp'],'C',' ',temp['P_Mag_Assy_Int_Temp'],'C',' ',temp['S_Trf_Center'],'C',' ',temp['Q_T_Amb'],'C',' ',temp['R_Int_Temp'],'C',' ',temp['T_Int_Amb'],'C'
    results.to_csv('Unit2 with Option B and Trf 03 Charge Discharge for New Fire Encl 2.csv')
    time.sleep(60)   # Delay in seconds before capturing results               
print('finished')