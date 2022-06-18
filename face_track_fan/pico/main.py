from machine import Pin, UART
import uos
import utime
from cloud_platform import CloudPlatform

"""
Raspberry Pi Pico/MicroPython + ESP-01S exercise

ESP-01S(ESP8266) with AT-command firmware:
AT version:1.7.4.0(June 15 2022 16:13:04)

Pico send AT command to ESP-01S via UART,
"""
server_ip = "192.168.0.105"
server_port = 5000

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

# indicate program started visually
led_onboard = Pin(25, Pin.OUT)
led_onboard.value(0)  # onboard LED OFF/ON for 0.5/1.0 sec
utime.sleep(0.5)
led_onboard.value(1)
utime.sleep(1.0)
led_onboard.value(0)

# 底部SG90伺服机引脚
pin_bottom = 16
# 顶部SG90伺服机引脚
pin_top = 17

# 创建一个云台对象
cp = CloudPlatform(pin_bottom, pin_top)

uart = UART(1, baudrate=115200, rx=Pin(5), tx=Pin(4), timeout=10)


def sendCMD_waitResp(cmd, uart=uart, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()


def waitResp(uart=uart, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms() - prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)


# send CMD to uart,
# wait and show response without return
def sendCMD_waitAndShow(cmd, uart=uart):
    print("CMD: " + cmd)
    uart.write(cmd)
    while True:
        print(uart.readline())


def espSend(text="test", uart=uart):
    sendCMD_waitResp('AT+CIPSEND=' + str(len(text)) + '\r\n')
    sendCMD_waitResp(text)


def XmonitorESP(uart=uart):
    """
    while True:
        line=uart.readline()
        try:
            print(line.decode())
        except UnicodeError:
            print(line)
    """
    while True:
        if uart.any():
            print(uart.read(1))


def ReceiveData():
    byte_raw = uart.read()
    #     print(byte_raw)
    if byte_raw is not None:
        s = byte_raw.decode()
        #         print(s)

        if s.find('+IPD') >= 0:
            n1 = s.find('<')
            n2 = s.find('>')
            bottom_angle = int(s[n1 + 1:n2])
            n3 = s.find('<', n1 + 1)
            n4 = s.find('>', n2 + 1)
            top_angle = int(s[n3 + 1:n4])
            print(bottom_angle, top_angle)
            return bottom_angle, top_angle

    return None, None


SSID = 'TP-LINK_4B0D'
password = 'weilixia2250wuguanmi'
ServerIP = '192.168.0.105'
Port = '5000'

sendCMD_waitResp('AT\r\n')  # 在启动之前，先发送一个AT命令，检查是否连接到了ESP-01S
sendCMD_waitResp('AT+GMR\r\n')  # 查询固件版本
# sendCMD_waitResp('AT+RESTORE\r\n')  # 恢复出厂设置

sendCMD_waitResp('AT+CWMODE?\r\n')  # 查询Wi-Fi模式
sendCMD_waitResp('AT+CWMODE=1\r\n')  # 设置Wi-Fi模式为Station模式
# sendCMD_waitResp('AT+CWMODE=2\r\n') # 设置Wi-Fi模式为2 = AP mode
sendCMD_waitResp('AT+CWMODE?\r\n')  # 再次查询Wi-Fi模式

# sendCMD_waitResp('AT+CWLAP\r\n', timeout=10000) # 列出所有可用的Wi-Fi热点
sendCMD_waitResp('AT+CWJAP="' + SSID + '","' + password + '"\r\n', timeout=5000)  # 连接到Wi-Fi热点
sendCMD_waitResp('AT+CIFSR\r\n')  # 查看本地IP地址
# sendCMD_waitResp("AT+CIPMUX=0\r\n") # 客户端必须是单连接模式
sendCMD_waitResp("AT+CIPMUX=1\r\n")  # 服务端模式
# sendCMD_waitResp("AT+CIPMODE=1\r\n") # 透传模式
# sendCMD_waitResp("AT+CIPSERVER=0,5000\r\n") # 客户端必须是单连接模式
sendCMD_waitResp("AT+CIPSERVER=1,5000\r\n")  # 服务端模式
# sendCMD_waitResp('AT+CIPSTART="TCP","192.168.0.102",9999\r\n')
# sendCMD_waitResp('AT+CIPSTART="TCP","' +
#                  server_ip +
#                  '",' +
#                  str(server_port) +
#                  '\r\n')  # 建立TCP连接到服务器


while True:
    if uart.any() < 6:
        # 如果缓存区不满6,就继续等待,因为传过来的数据格式是<角度><角度>
        continue

    if uart.any():
        bottom_angle, top_angle = ReceiveData()
        if bottom_angle is not None and \
                top_angle is not None and \
                cp.btm_max_angle >= bottom_angle >= cp.btm_min_angle and \
                cp.top_max_angle >= top_angle >= cp.top_min_angle:
            # 舵机云台执行相关动作
            cp.set_btm_servo_angle(bottom_angle)
            #             cp.set_top_servo_angle(top_angle)
            print("Bottom: {} Top: {}".format(bottom_angle, top_angle))

    #         sendCMD_waitResp('AT+CIPSTART="TCP","' +
    #                          server_ip +
    #                          '",' +
    #                          str(server_port) +
    #                          '\r\n')  # 建立TCP连接到服务器,如果作为TCP客户端时，才需要用到

    utime.sleep_ms(50)
