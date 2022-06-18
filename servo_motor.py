import RPi.GPIO as GPIO


class ServoMotor(object):
    """
    Servo motor type:
            ANNIMOS 20KG Digital Servo High Torque Full Metal Gear Waterproof for RC Model DIY, DS3218MG,Control Angle 270°
            2% duty cycle -> 0 degree
            12% duty cycle -> 270 degree
        Servo motor is only used for testing the calibration algorithm
    """
    control_channel = 26  # set GPIO 26 for output PWM to servo motor
    init_freq = 50  # initil frequency = 50Hz
    init_duty_cycle = 0  # set duty cycle as 2% (0 degree)
    cur_position = 0  # range (0 - 270 degree)
    name = 'servo_motor'

    def __init__(self, log):
        self.log = log  # initialize the logging
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.control_channel, GPIO.OUT)
        self.PWM = GPIO.PWM(self.control_channel, self.init_freq)
        self.PWM.start(self.init_duty_cycle)
        self.set_posiotion(200)
        time.sleep(2)
        self.log.info('servo initialization accomplished')

    def __del__(self):
        self.PWM.stop()
        GPIO.cleanup()

    def set_posiotion(self, position):
        '''
            PWM: the class initialized by GPIO.PWM
            angle: the angle you want to rotate (absolute position)
            2% duty cycle -> 0 degree
            12% duty cycle -> 270 degree
            angle/degree = duty cycle * 27 - 54
        '''
        if 0.0 <= position <= 270.0:
            duty_cycle = (position + 54.0) / 27.0
            self.PWM.ChangeDutyCycle(duty_cycle)
            self.cur_position = position
            log_str = 'current position:' + str(self.cur_position)
            self.log.info(log_str)
            self.log.info('current_position=%d degree' % (self.cur_position))
            time.sleep(1)  # wait one second to reach the position
        else:
            self.log.warning("invalid rotation angle")

    def move(self, move_angle, direction):
        if move_angle < 0 or self.cur_position + move_angle > 270:
            self.log.error("exceed the 270 degree")
            return False
        move_angle = -move_angle if direction == 'CW' else move_angle
        self.set_posiotion(self.cur_position + move_angle)
        self.log.info('move_angle=%d degree, direction=%s' % (abs(move_angle), direction))
        return True

    def get_motor_type(self):
        return self.name
