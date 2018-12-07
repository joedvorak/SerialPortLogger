#!/usr/bin/env python3

import os
import serial
import time
import datetime

#Try to open the Serial Port. If it is not connected, retry after 2 sec, forever.
while True:
    for p in range (0,10):
        portname = "/dev/ttyACM" + str(p)
        try:
            ser = serial.Serial(portname,
                            baudrate = 115200, 
                            parity=serial.PARITY_NONE,  
                            bytesize = serial.EIGHTBITS,
                            stopbits = serial.STOPBITS_ONE,
                            timeout = 1
                            )
            print('Hybrid Controller found on ' + portname)
            i = 0
            while os.path.exists("/home/pi/hybridLogs/log%s.csv" % i):
                i += 1
            datafile = open("/home/pi/hybridLogs/log%s.csv" % i, "w")
            while True:
                try:    
                    lineIn = ser.readline()
                except serial.serialutil.SerialException:
                        print('Hybrid Controller unplugged')
                        datafile.close()
                        break
                try:
                    datastr=lineIn.decode()
                except UnicodeDecodeError:
                    print('Error on line. Trying next line')
                else:
                    writestr = str(datetime.datetime.now())+"\t" + datastr
                    print(writestr)
                    datafile.write(writestr)
                    datafile.flush()        
        except serial.serialutil.SerialException:
            print('Hybrid Controller not attached on ' + portname)
            time.sleep(2)


    