#===============================================================================
# #  load required modules
#===============================================================================

import os
import glob
import time
import requests
import json
import string
import datetime
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensor_id = ''
sensor_desc = ''
color = ''

#===============================================================================
# #  define global variables
#===============================================================================

url = 'anyurl'
headers = {"Content-type": 'application/json;charset=utf-8'}
auth = 'USER', 'PW'

base_dir = '/sys/bus/w1/devices/'
collection = glob.glob(base_dir + '28*')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#===============================================================================
# #  some required functions
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
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
#    return temp_c, temp_f

#===============================================================================
# #  start loop over sensor directories
#===============================================================================

 for x in collection:

#   print x
  sensor_id = string.replace(x, base_dir, '')

  if sensor_id == '28-00000511359a':
    sensor_desc = "Aussentemp\t"
    color = "1"
  if sensor_id == '28-00000510d317':
    sensor_desc = "Innentemp\t"
    color = "2"

  sensor_id = "'" + sensor_id + "'"

  dt = int(time.time())
  var = datetime.datetime.fromtimestamp(dt)

  v_date = "'" + "/Date(" + str(dt)  + "000)/" + "'"
  v_time = var.strftime('PT%HH%MM%SS')
  v_time = "'" + str(v_time) + "'"

  device_file = x + '/w1_slave'

  temp = "'" + str(read_temp()) + "'"
  temperatur = str(read_temp())
#===============================================================================
# output to console
#===============================================================================
  f = open('wetterstation/wetterdaten.json','w')
  if color == '1':
    f.write(temperatur)
    print bcolors.OKGREEN + sensor_desc, sensor_id, v_date, v_time, temp + bcolors.ENDC
    print temperatur

  if color == '2':
    print sensor_desc, sensor_id, v_date, v_time, temp

  f.close() # you can omit in most cases as the destructor will call if

#===============================================================================
# #  build payload
#===============================================================================

  payload = "{ 'SENSOR_ID': " + sensor_id + " , 'DATE': " + v_date + " , 'TIME': " + v_time + " , 'VALUE': " + temp + " }"
  payload = payload.replace("'",'"')

#  print payload

#=============================================================================
# send message to HANA Buechse :-)
#=============================================================================
#  try:
#    r = requests.post(url, data=payload, headers=headers, auth=auth)
#  except:
#    print bcolors.WARNING + "Post to Hana Error\t" + v_time + bcolors.ENDC
#  print r.text
