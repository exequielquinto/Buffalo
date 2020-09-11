import visa, time

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x0455::C011137::0::INSTR')
print scope.query('*IDN?')

x=100

#scope.write('HARDCOPY:INKSAVER ON')      #NOT WORKING

#Change horizontal scale to any value

scope.write('HOR:SCA 200')
time.sleep(1)
#scope.write('HOR:SCA 2e-6')

#SINGLE
#scope.write('ACQ:STOPA SEQ')
#scope.write('ACQ:STATE Single')
#print 2
#ime.sleep(5)

#RUN
scope.write('ACQ:STATE ON')
print 3
time.sleep(20)

#STOP
scope.write('ACQ:STATE OFF')
print 4
time.sleep(5)

scope.write('SAVE:IMAG:FILEF PNG')
scope.write('HARDCOPY START')
raw_data = scope.read_raw()

fid = open('tek00'+str(x)+'.png','wb')
#fid = open('Unit2_30_0'+'.png','wb')
#fid = open('normal @ 340V min load'+'.png','wb')
fid.write(raw_data)
fid.close()

#print('???')

#scope.write(":MEAS:SOUR CHAN1")
# Grab VMAX
#v_max = scope.query_ascii_values(":MEAS:ITEM? VMAX")
#print v_max

#print scope.query('DATA:SOURCE?')
#print scope.write('MEASU:MEAS1:VAL?')
#print scope.write('CURVE?')

#print scope.write('MEASU:MEAS3:VAL?')
#print scope.write('MEASure:VMAX %s' % ('CHANNEL3'))
#print 1
#temp_values = scope.query_ascii_values(':MEASure:VMAX? %s' % ('CHANNEL3'))
#print temp_values
#print scope.ask('MEASU:VMAX:VAL')
#print float(scope.read())


print('finish')