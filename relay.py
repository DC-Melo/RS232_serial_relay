#!/usr/bin/env python
# coding=utf-8
##########################################################################
# AUTHOR   : DC-Melo
# MAIL     : melo.da.chor@gmail.com
# BLOG     : www.dc-melo.com
# FILE     : cantest.py
# CREATED  : 2020-11-10 15:50
# MODIFIED : 2020-11-27 11:31
# VERSION  : V-0.0.2.201127_a:add opt parameter function;V-0.0.1.201110_a: ;
# DESCRIB  : 
# NOTICES  : 
##########################################################################
# from __future__ import print_function
import os
import sys
import platform
import time
import re
import serial #导入模块
import serial.tools.list_ports
from binascii import *
from crcmod import *

# CRC16-MODBUS
def crc16Add(read):
    crc16 =crcmod.mkCrcFun(0x18005,rev=True,initCrc=0xFFFF,xorOut=0x0000)
    data = read.replace(" ","")
    readcrcout=hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2,'0')      # 位数不足补0
    crc_data = "".join(str_list)
    read = read.strip()+' '+crc_data[4:]+' '+crc_data[2:4] # 十六进制反转
    return read

if __name__ == '__main__':
    while 1:
        ser1=serial.Serial("/dev/ttyS0",9600,timeout=0.5)
        for module in range(1,2): # 循环模块
            for relay in range(0,8): # 循环每个模块继电器
                command_val=[module,5,0,relay,255,0] # 开继电器
                command_hex=['{:02x}'.format(item) for item in command_val]
                command_crc=crc16Add(" ".join(command_hex))
                print(command_crc)
                result=ser1.write(bytes.fromhex(command_crc))#写数据
                print("send relay:",command_crc)
                time.sleep(1)
            command_val=[module,15,0,0,0,16,2,0,0] 
            command_hex=['{:02x}'.format(item) for item in command_val] # 转为十六进制
            command_crc=crc16Add(" ".join(command_hex)) # 拼接发送数据
            result=ser1.write(bytes.fromhex(command_crc)) # 写数据
            print("send relay:",command_crc)
            time.sleep(1)
            command_val=[module,15,0,0,0,16,2,255,255] # 关继电器
            command_hex=['{:02x}'.format(item) for item in command_val]
            command_crc=crc16Add(" ".join(command_hex))
            result=ser1.write(bytes.fromhex(command_crc))
            print("send relay:",command_crc)
            time.sleep(1)
        for module in range(1,2):
            for relay in range(0,8):
                command_val=[module,5,0,relay,0,0]
                command_hex=['{:02x}'.format(item) for item in command_val]
                command_crc=crc16Add(" ".join(command_hex))
                result=ser1.write(bytes.fromhex(command_crc))
                print("send relay:",command_crc)
                time.sleep(1)
                
            command_val=[module,15,0,0,0,16,2,255,255]
            command_hex=['{:02x}'.format(item) for item in command_val]
            command_crc=crc16Add(" ".join(command_hex))
            result=ser1.write(bytes.fromhex(command_crc))#写数据
            print("send relay:",command_crc)
            time.sleep(1)
            command_val=[module,15,0,0,0,16,2,0,0]
            command_hex=['{:02x}'.format(item) for item in command_val]
            command_crc=crc16Add(" ".join(command_hex))
            result=ser1.write(bytes.fromhex(command_crc))#写数据
            print("send relay:",command_crc)
            time.sleep(1)

        ser1.close()
        time.sleep(2)
