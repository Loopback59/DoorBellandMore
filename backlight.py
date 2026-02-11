import RPi.GPIO as GPIO
import subprocess
from time import sleep, localtime, strftime

SensorPin = 18
DisplayOnTime = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(SensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


Timer = DisplayOnTime


def BacklightON():
    subprocess.run(["/home/martin/bon.sh"],shell=True)

def BacklightOFF():
    subprocess.run(["/home/martin/boff.sh"],shell=True)


m = int(strftime("%M", localtime()))
oldMinute = m

while (1):

    #s = int(strftime("%S", localtime()))
    m = int(strftime("%M", localtime()))
    #h = int(strftime("%H", localtime()))

    if (m % 1) == 0 and (oldMinute != m):
        oldMinute = m
        if Timer > 0:
            Timer = Timer - 1
            #print("countdown = ",Timer)
        else:
            BacklightOFF()


    if GPIO.input(SensorPin) == True:
        Timer = DisplayOnTime
        BacklightON()

    sleep(0.1)


"""
{"id":0, "source":"MQTT", "output":false,"temperature":{"tC":45.3, "tF":113.6}}
{"id":0, "source":"WS_in", "output":true,"temperature":{"tC":47.2, "tF":116.9}}
"""

"""
OK now you can set the GPIO #18 pin to PWM mode using WiringPi's gpio command

With these basic shell commands, you can set the GPIO #18 pin to PWM mode with 1000 Hz frequency,
set the output to 100 (out of 1023, so dim!), set the output to 1023
(out of 1023, nearly all the way on) and 0 (off)

gpio -g mode 18 pwm
gpio pwmc 1000
gpio -g pwm 18 100
gpio -g pwm 18 1023
gpio -g pwm 18 0

"""
