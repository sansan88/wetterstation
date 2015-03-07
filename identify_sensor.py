
#===============================================================================
# #  load required modules
#===============================================================================

import os
import glob
import time
import json

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#===============================================================================
# #  start loop over sensor directories
#===============================================================================

while True:

 def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

 def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
#    return temp_c, temp_f

 base_dir = '/sys/bus/w1/devices/'

 collection = glob.glob(base_dir + '28*')

 for x in collection:

  print x
  device_file = x + '/w1_slave'

#===============================================================================
# #  output found sensors
#===============================================================================

  print(read_temp())
