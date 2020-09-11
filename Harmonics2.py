import visa, time

#Connect to Instruments
rm = visa.ResourceManager()
meter = rm.open_resource('USB0::0x0B21::0x0025::39314E343038383731::0::INSTR') #USB0::0x0B21::0x0025::55314A383031393531::0::INSTR')
#(u'USB0::2849::37::39314E343038383731::0::INSTR', u'USB0::2849::37::55314A383031393531::0::INSTR')

meter.write(':NUMERIC:FORMAT ASCII')

meter.write(':NUMeric:HOLD ON')
#meter.write(':HARMONICS:PLLSOURCE V1')   #works
meter.write(':NUMeric:LIST:NUMber 1')
meter.write(':NUMERIC:LIST:ORDER 40')   #works
#meter.write(':NUMERIC:ORDER 1,40')
meter.write(':NUMERIC:LIST:SELECT ALL')  #works
#meter.write(':NUMERIC:LIST:VALUE? 1')

print meter.query(':HARMONICS:THD?')
print meter.query(':HARMONICS?')

meter.write(':NUMeric:NORMal:ITEM1 ITHD,1;')

#print float(meter.query(':NUMERIC:NORMAL:VALUE? 1'))

x = (meter.query(':NUMERIC:LIST:VALUE?'))
print x

#print float(x[0:9])

#print meter.write(':NUMeric:NORMal:ITEM1 URMS,1;ITEM2 IRMS,1;ITEM3 LAMBda,1;ITEM4 P,1;ITEM5 UDC,2;ITEM6 IDC,2;ITEM7 P,2;ITEM8 ITHD,1;ITEM9 UDC,3;ITEM10 IDC,3;ITEM11 P,3;')
#print meter.query(':NUMeric:NORMal:VALue?')

#meter.write(':NUMeric:HOLD OFF')