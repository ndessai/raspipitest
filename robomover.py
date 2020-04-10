from __future__ import division
from cmdmoves import CommandType, MotionType, MotionCommand, StartCommand, StopCommand 
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685
import ultra
import RGB

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17
Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

pwn_A = 0
pwm_B = 0

'''
change this form 1 to 0 to reverse servos
'''
pwm0_direction = -1
pwm1_direction = 1
pwm2_direction = 1

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm0_init = 300
pwm0_range = 100
pwm0_max  = 500
pwm0_min  = 100
pwm0_pos  = pwm0_init

pwm1_init = 300
pwm1_range = 150
pwm1_max  = 450
pwm1_min  = 150
pwm1_pos  = pwm1_init

pwm2_init = 300
pwm2_range = 150
pwm2_max  = 450
pwm2_min  = 150
pwm2_pos  = pwm2_init

class RoboMover:

    def __init__(self):
        self.setup()
        RGB.setup()
        RGB.cyan()
        try:
            pwm.set_all_pwm(0, 300)
        except:
            pass
        pwm.set_pwm(0, 0, pwm0_init)
        pwm.set_pwm(1, 0, pwm1_init)
        pwm.set_pwm(2, 0, pwm2_init)

    def motorStop(self):#Motor stops
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)


    def setup(self):#Motor initialization
        global pwm_A, pwm_B
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.motorStop()
        try:
            pwm_A = GPIO.PWM(Motor_A_EN, 1000)
            pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        except:
            pass


    def motor_A(self, direction, speed):#Motor 2 positive and negative rotation
        if direction == Dir_backward:
            GPIO.output(Motor_B_Pin1, GPIO.HIGH)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)
        elif direction == Dir_forward:
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.HIGH)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)


    def motor_B(self, direction, speed):#Motor 1 positive and negative rotation
        if direction == Dir_forward:#
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            pwm_B.start(100)
            pwm_B.ChangeDutyCycle(speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            pwm_B.start(0)
            pwm_B.ChangeDutyCycle(speed)

    def replace_num(self, initial,new_num):   #Call this function to replace data in '.txt' file
        newline=""
        str_num=str(new_num)
        with open("%s/servo.py"%sys.path[0],"r") as f:
            for line in f.readlines():
                if(line.find(initial) == 0):
                    line = initial+"%s\n"%(str_num)
                newline += line
        with open("%s/servo.py"%sys.path[0],"w") as f:
            f.writelines(newline)	#Call this function to replace data in '.txt' file


    def turnLeft(self, coe=1):
        global pwm2_pos
        pwm2_pos = pwm2_init + int(coe*pwm2_range*pwm2_direction)
        pwm2_pos = self.ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        RGB.both_off()
        RGB.yellow()
        print(pwm2_pos)
        pwm.set_pwm(2, 0, pwm2_pos)


    def turnRight(self, coe=1):
        global pwm2_pos
        pwm2_pos = pwm2_init - int(coe*pwm2_range*pwm2_direction)
        pwm2_pos = self.ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        RGB.both_off()
        RGB.yellow()
        pwm.set_pwm(2, 0, pwm2_pos)


    def turnMiddle(self):
        global pwm2_pos
        pwm2_pos = pwm2_init
        RGB.both_on()
        pwm.set_pwm(2, 0, pwm2_pos)


    def setPWM(self, num, pos):
        global pwm0_init, pwm1_init, pwm2_init, pwm0_pos, pwm1_pos, pwm2_pos
        pwm.set_pwm(num, 0, pos)
        if num == 0:
            pwm0_init = pos
            pwm0_pos = pos
        elif num == 1:
            pwm1_init = pos
            pwm1_pos = pos
        elif num == 2:
            pwm2_init = pos
            pwm2_pos = pos


    def saveConfig(self):
        RGB.pink()
        self.replace_num('pwm0_init = ',pwm0_init)
        self.replace_num('pwm1_init = ',pwm1_init)
        self.replace_num('pwm2_init = ',pwm2_init)
        RGB.cyan()


    def radar_scan(self):
        global pwm1_pos
        RGB.cyan()
        scan_result = 'U: '
        scan_speed = 1
        if pwm1_direction:
            pwm1_pos = pwm1_max
            pwm.set_pwm(1, 0, pwm1_pos)
            time.sleep(0.5)
            scan_result += str(ultra.checkdist())
            scan_result += ' '
            while pwm1_pos>pwm1_min:
                pwm1_pos-=scan_speed
                pwm.set_pwm(1, 0, pwm1_pos)
                scan_result += str(ultra.checkdist())
                scan_result += ' '
            pwm.set_pwm(1, 0, pwm1_init)
            pwm1_pos = pwm1_init
        else:
            pwm1_pos = pwm1_min
            pwm.set_pwm(1, 0, pwm1_pos)
            time.sleep(0.5)
            scan_result += str(ultra.checkdist())
            scan_result += ' '
            while pwm1_pos<pwm1_max:
                pwm1_pos+=scan_speed
                pwm.set_pwm(1, 0, pwm1_pos)
                scan_result += str(ultra.checkdist())
                scan_result += ' '
            pwm.set_pwm(1, 0, pwm1_init)
            pwm1_pos = pwm1_init
        RGB.both_on()
        return scan_result


    def ctrl_range(self, raw, max_genout, min_genout):
        if raw > max_genout:
            raw_output = max_genout
        elif raw < min_genout:
            raw_output = min_genout
        else:
            raw_output = raw
        return int(raw_output)


    def lookleft(self, speed):
        global pwm1_pos
        pwm1_pos += speed*pwm1_direction
        pwm1_pos = self.ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        pwm.set_pwm(1, 0, pwm1_pos)


    def lookright(self, speed):
        global pwm1_pos
        pwm1_pos -= speed*pwm1_direction
        pwm1_pos = self.ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        pwm.set_pwm(1, 0, pwm1_pos)


    def up(self, speed):
        global pwm0_pos
        pwm0_pos -= speed*pwm0_direction
        pwm0_pos = self.ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        pwm.set_pwm(0, 0, pwm0_pos)


    def down(self, speed):
        global pwm0_pos
        pwm0_pos += speed*pwm0_direction
        pwm0_pos = self.ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        pwm.set_pwm(0, 0, pwm0_pos)

    def ahead(self):
        global pwm1_pos, pwm0_pos
        pwm.set_pwm(1, 0, pwm1_init)
        pwm.set_pwm(0, 0, pwm0_init)
        pwm1_pos = pwm1_init
        pwm0_pos = pwm0_init


    def get_direction(self):
        return (pwm1_pos - pwm1_init)

    def Done(self):
        global pwm
        self.motorStop()
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(50)
        pwm.set_all_pwm(0, 0)
        GPIO.cleanup()             # Release resource


    def Move(self, command):
        if command.commandType != CommandType.Motion:
            return
        if command.motionType == MotionType.MoveForward:
            self.motor_A(0, command.speed)
            self.motor_B(1, command.speed)
            time.sleep(command.duration)
            self.motorStop()
        if command.motionType == MotionType.MoveBackward:
            self.motor_A(1, command.speed)
            self.motor_B(0, command.speed)
            time.sleep(command.duration)
            self.motorStop()

        if command.motionType == MotionType.MoveLeft:
            self.turnLeft(command.speed)
        if command.motionType == MotionType.MoveRight:
            self.turnRight(command.speed)
        if command.motionType == MotionType.MoveCenter:
            self.turnMiddle()

        if command.motionType == MotionType.LookRight:
            self.lookright(command.speed)
        if command.motionType == MotionType.LookLeft:
            self.lookleft(command.speed)
        if command.motionType == MotionType.LookHCenter:
            self.ahead()

        if command.motionType == MotionType.LookUp:
            self.up(command.speed)
        if command.motionType == MotionType.LookDown:
            self.down(command.speed)
        if command.motionType == MotionType.LookVCenter:
            self.ahead()
