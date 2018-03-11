#!/usr/bin/env python
import math
import time
import datetime
import subprocess

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
#image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
wifi = Image.open('/home/pi/info/wifi.ppm').convert('1')
#Create drawing object.
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
import os
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
def getCPUuse():
    return(str(os.popen("top -bn1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
while True:
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        if "SSID:" in os.popen("iwconfig wlan0 | grep SSID").read():
                image.paste(wifi)
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()
        RAM_stats = getRAMinfo()
        RAM_total = int(int(RAM_stats[0]) / 1024)
        RAM_used = int(int(RAM_stats[1]) / 1024)
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        v1='Temp:'+CPU_temp
        v2='CPU:'+CPU_usage+'%'
        v3='RAM:'+str(RAM_used) + 'M' + '/'+str(RAM_total)+'M'
        v4='Dysk:'+DISK_used+'/'+DISK_total
        now= datetime.datetime.now()
        data=now.strftime("%d-%m-%Y")
        czas=now.strftime("%H:%M:%S")
        draw.text((0,0), data, font=font)
        draw.text((0,7), czas, font=font)
        draw.text((0,15), v1, font=font)
        draw.text((0,23), v2, font=font)
        draw.text((0,31), v3, font=font)
        draw.text((0,39), v4, font=font)
        disp.image(image)
        disp.display()
