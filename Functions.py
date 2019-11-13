import struct, time

def float32_to_bin(num):
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)

def bin_to_float32(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def dec_to_bin(msb,lsb):
    x=bin(int(msb))
    y=bin(int(lsb))
    return str(x)[2:18].zfill(16)+str(y)[2:18].zfill(16)

def dec_to_float32(msb,lsb):
    return bin_to_float32(dec_to_bin(msb, lsb))

def float32_to_msb(num):
    return int(float32_to_bin(num)[0:16],2)

def float32_to_lsb(num):
    return int(float32_to_bin(num)[16:32],2)

def pac_set(msb,lsb,client):
    try:
        client.write_register(5054, msb)
        client.write_register(5055, lsb)
    except:
        try:
            print('pac set error1')
            client.write_register(5054, msb)
            client.write_register(5055, lsb)
        except:
            print('pac set error2')
            client.write_register(5054, msb)
            client.write_register(5055, lsb)
 
ref_time=time.time()
def measure(temp, meter):
    #Time
    temp['A_Time']=time.ctime()
    
    #Minutes
    temp['B_Mins']=round((time.time()-ref_time)/60)
    
    #Yokogawa Power Analyzer
    meter.write(':NUMeric:HOLD ON')
    meter.write(':NUMeric:NORMal:ITEM1 URMS,1;ITEM2 IRMS,1;ITEM3 LAMBda,1;ITEM4 P,1;ITEM5 UDC,2;ITEM6 IDC,2;ITEM7 P,2;ITEM8 ITHD,1;ITEM9 UDC,3;ITEM10 IDC,3;ITEM11 P,3;')
    
    #Measure Vac
    Vac = float(meter.query(':NUMERIC:NORMAL:VALUE? 1'))
    temp['C_Vac'] = Vac
    
    #Measure Iac
    Iac = float(meter.query(':NUMERIC:NORMAL:VALUE? 2'))
    temp['D_Iac'] = Iac
    
    #Measure P_Factor
    PF = float(meter.query(':NUMERIC:NORMAL:VALUE? 3'))
    temp['E_PF'] = PF    
    
    #Measure Pac
    Pac = float(meter.query(':NUMERIC:NORMAL:VALUE? 4'))
    temp['F_Pac'] = Pac
    
    #Measure Batt Vdc
    Vdc = float(meter.query(':NUMERIC:NORMAL:VALUE? 5'))
    temp['G_Vdc'] = Vdc
   
    #Measure Batt Idc
    Idc = float(meter.query(':NUMERIC:NORMAL:VALUE? 6'))
    temp['H_Idc'] = Idc
    
    #Measure Batt Pdc
    Pdc = float(meter.query(':NUMERIC:NORMAL:VALUE? 7'))
    temp['I_Pdc'] = Pdc
    
    #Measure Eff
    if abs(Pdc) > abs(Pac):
        temp['J_Eff'] = (Pac*100)/Pdc
    else:
        temp['J_Eff'] = (Pdc*100)/Pac
    
    #Measure ITHD
    Ithd = float(meter.query(':NUMERIC:NORMAL:VALUE? 8'))
    temp['K_Ithd'] = Ithd
    
    #Measure Vaux
    Vaux = float(meter.query(':NUMERIC:NORMAL:VALUE? 9'))
    temp['L_Vaux'] = Vaux
   
    #Measure Iaux
    Iaux = float(meter.query(':NUMERIC:NORMAL:VALUE? 10'))
    temp['M_Iaux'] = Iaux
    
    #Measure Paux
    Paux = float(meter.query(':NUMERIC:NORMAL:VALUE? 11'))
    temp['N_Paux'] = Paux
    
    meter.write(':NUMeric:HOLD OFF')   
    
def harmonics(temp, meter):
    #Time
    temp['A_Time']=time.ctime()
    
    #Minutes
    temp['B_Mins']=round((time.time()-ref_time)/60)
    
    #Yokogawa Power Analyzer
    #Measure Harmonics
    meter.write(':NUMeric:HOLD ON')
    meter.write(':HARMONICS:PLLSOURCE I1')   #works
    meter.write(':NUMeric:LIST:NUMber 1')
    meter.write(':NUMERIC:LIST:ORDER 40')   #works
    #meter.write(':NUMERIC:ORDER 1,40')
    meter.write(':NUMERIC:LIST:SELECT ALL')  #works
    #meter.write(':NUMERIC:LIST:VALUE? 1')
    temp['C_Harmonics'] = (meter.query(':NUMERIC:LIST:VALUE?'))
    
    #Measure ITHD
    meter.write(':NUMeric:NORMal:ITEM1 ITHD,1;')
    temp['D_ITHD'] = float(meter.query(':NUMERIC:NORMAL:VALUE? 1'))
   
    meter.write(':NUMeric:HOLD OFF')         