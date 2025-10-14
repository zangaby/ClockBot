from ht16k33 import HT16K33
from machine import I2C, Pin
from time import sleep
from ht16k33.scroller import Scroller


import machine
import network
import sys
import time
import usocket as socket
import ustruct as struct
from machine import RTC

# WLAN-Configuration
wlanSSID = 'xxxx'
wlanPW = 'xxx'
network.country('XX')
rtc = RTC()

#year, month, day, hour, mins, secs, weekday, yearday = time.localtime()

# Wintertime / Sommertime
#GMT_OFFSET = 3600 * 1 # 3600 = 1 h (Wintertime)
GMT_OFFSET = 3600 * 2 # 3600 = 1 h (Sommertime)

# Status-LED
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)

# NTP-Host
NTP_HOST = 'pool.ntp.org'

# Function: WLAN-Connection
def wlanConnect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('Connecting...')
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            led_onboard.toggle()
            print('.')
            time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Status:', wlan.status())
        led_onboard.on()
    else:
        print('No WLAN connection')
        led_onboard.off()
        print('WLAN-Status:', wlan.status())

# Function: Get NTP Time
def getTimeNTP():
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = struct.unpack("!I", msg[40:44])[0]
    return time.gmtime(ntp_time - NTP_DELTA + GMT_OFFSET)

# Function: Set NTP Time
def setTimeRTC():
    # Get NTP Time
    tm = getTimeNTP()
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

# Connect to WiFi
wlanConnect()

# Set Time
setTimeRTC()

id = 0
sda = Pin(0)
scl = Pin(1)
address = 0x70

i2c = I2C(id, sda=sda, scl=scl)
matrix = HT16K33(i2c)


def blink(times):
    speed = 1.0
    for _ in range(times):
        matrix.show_icon("happy")
        sleep(speed)
        matrix.clear()
        matrix.show_icon("eyes_closed")
        sleep(speed/2)
        matrix.show_icon("happy")
        sleep(speed)
        matrix.clear()
#     matrix.clear()

def get_time():
#    datetime = time.localtime()
#    hour =  str(datetime[4])
#    minute = str(datetime[5])
    #time = hour + ':' + minute
    datetime = rtc.datetime()
    hour =  str(datetime[4])
    minute = str(datetime[5])
    time = hour + ':' + minute
    #time = "{}:{:02d}".format(hour, mins)
    print(time)

def pulse_heart(times):

    for _ in range(times):
        matrix.show_icon("heart")
        sleep(0.1)
        matrix.clear()
        matrix.show_icon("small_heart")
        sleep(0.1)
        matrix.clear()
    matrix.clear()

def sleepy_time():
    matrix.show_icon("happy")
    sleep(0.5)
    matrix.show_icon("sleepy")
    sleep(0.5)
    matrix.show_icon("eyes_closed")
    sleep(1)

def show_message(message):
    scroll.num_cols = 8
    scroll.num_rows = 8
    for position in range(0, -len(message*(scroll.num_cols)), -1):

        matrix.clear()
        matrix.auto_write = False
        scroll.show_message(message, position)
        matrix.update()
        sleep(0.05)

def demo():
    matrix.show_icon("happy")
    sleep(1)
    blink(2)
    sleep(1)
    matrix.show_icon("smile")
    sleep(1)
    pulse_heart(10)
    time = '       ' + "{}:{:02d}".format(hour, mins)
    message = time
    print(message)
    show_message(message)
    pulse_heart(10)
scroll = Scroller(matrix)
while True:
      year, month, day, hour, mins, secs, weekday, yearday = time.localtime()
      demo()