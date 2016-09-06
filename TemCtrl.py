# -*- coding: utf-8 -*-

import serial.tools.list_ports
import time
import crcmod
import binascii
import datetime
from msvcrt import getch
import thread


global ReadTem

############ Check Com Port ###################################################
def serial_ports():

    ports = list(serial.tools.list_ports.comports())

    port_all =""

    # return the port if 'USB' is in the description
    for port_no, description, address in ports:
        if 'USB' in description:
            port_all = port_all+' '+port_no
    return port_all.split()

####To determin ComPort
def getComPort():

    SerPort = serial_ports()
    ComPort = ''
    if len(SerPort)>0:
        for i in SerPort:
            try:
                ser = serial.Serial(port=i, baudrate=9600, 	timeout=0.2,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
                ser.write('\x01\x04\x00\x00\x00\x01\x31\xca')
                s = ser.read(7)
                rx = s.encode("hex")

                if len(rx)>1:
                    ComPort=i

                    print 'Connected to COM Port:', ComPort
                    break
            except serial.SerialException:
                print 'Check your connection!!!'
                time.sleep(10)

            else:
                print "{} may not be the device, please check the connection!!! This window will be closed in 20 seconds".format(i)
                time.sleep(20)
                return ComPort
        ser.close()
    else:
        print "No device was detected, please check the connection!!! This window will be closed in 20 seconds"
        time.sleep(20)
    return ComPort


############ Set the Temperature ###########################################
def setTem():
    ##### Get the Checksum
    ##十进制转换为16进制
    print 'Please input temperature: '
    temperature = int(raw_input())*10
    temperature_hex =  "{:04x}".format(temperature)
    temperature_final = r'01060000' + temperature_hex

    ##得到checksum
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    checkSum_dec = crc16(binascii.a2b_hex(temperature_final))
    checkSum_hex = "{:04x}".format(checkSum_dec)
    checksum = checkSum_hex[2:4] +checkSum_hex[0:2]     ## MSB和LSB调回来

    temperature_cmd = temperature_final+checksum
    # ser = serial.Serial(port=COM, baudrate=9600, timeout=0.2, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
    ser.write(binascii.a2b_hex(temperature_cmd))
    # ser.close()



########### Read the Temperature ##############
def readTem(interval):
    global ser

    while True:
        ser = serial.Serial(port=COM, baudrate=9600, timeout=0.2, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
        ser.write('\x01\x04\x00\x00\x00\x01\x31\xca')
        s = ser.read(7)
        rx = s.encode("hex")

        ##Temperature Reading
        ReadTem = int(rx[6:10],16)
        ReadTem =float(ReadTem)/10

        ########## Write ReadTem to file
        current_time  = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        current_time_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        filename = 'Temperature' + '_'+ current_time_filename +'.txt'
        f = open(filename, 'a')
        f.write(current_time + '\t')
        f.write(str(ReadTem) + '\n')
        #################################

        print current_time +'\t' + str(ReadTem) + ' '+ u'\u2103'
        time.sleep(interval)

        ser.close()

def keypress():

    while True:

        key = ord(getch())

        if key == 27:  #ESC
            break
        elif key == 13:  # Enter
            print 'Wanna set temperature? Y/N: '
            input_cmd1 = raw_input()
            if input_cmd1 == 'N' or input_cmd1 == 'n':
                pass
            elif input_cmd1 == 'Y' or input_cmd1 == 'y':
                setTem()
            time.sleep(2)

######### Main function ################################
#///////////////////// All the input////////////////////////////////////////////////////////////

interval = 2  #reading temperature every 'interval' seconds

#/////////////////////////////////////////////////////////////////////////////////////////////

COM=getComPort()
thread.start_new_thread(keypress, ())   #creat a new thread
readTem(interval)





