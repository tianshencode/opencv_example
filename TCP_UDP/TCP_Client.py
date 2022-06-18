from machine import UART, Pin
import utime,time

SSID='TP-LINK_4B0D'
password = 'weilixia2250wuguanmi'
ServerIP = '192.168.0.103'
Port = '5000'

uart = UART(1, baudrate=115200, rx=Pin(5), tx=Pin(4), timeout=10)


def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
            print(s)
            if(s.find(ack) >= 0):
                return True
    return False

uart.write('+++')
time.sleep(1)
if(uart.any()>0):uart.read()
sendCMD("AT","OK")
sendCMD("AT+CWMODE=3","OK")
sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
sendCMD("AT+CIFSR","OK")
sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000)
sendCMD("AT+CIPMODE=1","OK")
sendCMD("AT+CIPSEND",">")

uart.write('Hello World !!!\r\n')
uart.write('ESP8266 TCP Client\r\n')
while True:
    s=uart.read()
    if(s != None):
        s=s.decode()
        print(s)
