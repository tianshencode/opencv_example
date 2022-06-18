# -*- coding:utf-8 -*-

'''
二自由度云台
2DOF
'''
from machine import PWM, Pin


class CloudPlatform(object):
    def __init__(self, gpio_btm, gpio_top, freq=50):

        self.servos_btm = PWM(Pin(gpio_btm))
        self.servos_top = PWM(Pin(gpio_top))
        self.servos_btm.freq(freq)
        self.servos_top.freq(freq)
        self.btm_min_angle = 0  # 底部舵机最小旋转角度
        self.btm_max_angle = 180  # 底部舵机最大旋转角度
        self.btm_init_angle = 90  # 底部舵机的初始角度
        self.top_min_angle = 0  # 顶部舵机的最小旋转角度
        self.top_max_angle = 180  # 顶部舵机的最大旋转角度
        self.top_init_angle = 180  # 顶部舵机的初始角度

        # 初始化云台角度
        self.init_cloud_platform()

    def set_btm_servo_angle(self, angle):
        '''
        设定云台底部舵机的角度
        '''
        if angle < self.btm_min_angle:
            angle = self.btm_min_angle
        elif angle > self.btm_max_angle:
            angle = self.btm_max_angle

        duty_u16 = int((2.5 + angle * 10 / 180) / 100 * 65532)
        self.servos_btm.duty_u16(duty_u16)

    def set_top_servo_angle(self, angle):
        '''
        设定云台顶部舵机的角度
        '''
        if angle < self.top_min_angle:
            angle = self.top_min_angle
        elif angle > self.top_max_angle:
            angle = self.top_max_angle

        duty_u16 = int((2.5 + angle * 10 / 180) / 100 * 65532)
        self.servos_top.duty_u16(duty_u16)

    def init_cloud_platform(self):
        self.set_btm_servo_angle(self.btm_init_angle)
        self.set_top_servo_angle(self.top_init_angle)

