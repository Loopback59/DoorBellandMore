from time import sleep, localtime, strftime
import RPi.GPIO as GPIO

# GPIO pins
MovementDetector = 18   # Input from movement sensor USED IN BACKLIGHT.PY

DoorbellButton   = 21     # Input from button
DoorbellLed      = 2         # Output to lit the button Led

DoorbellRelay    = 26      # Output for doorbell relay
AnotherRelay     = 20      # Outpur for Relay #2



def Button_callback(gpio_id):
    # Disable so we don't queue up stuff
    GPIO.remove_event_detect(DoorbellButton)

    GPIO.output(DoorbellRelay, GPIO.HIGH)   # Ding
    sleep(0.4)
    GPIO.output(DoorbellRelay, GPIO.LOW)    # Dong
    sleep(0.1)

    #Logg the doorbell here

    GPIO.add_event_detect(DoorbellButton, GPIO.FALLING, bouncetime=200)
    GPIO.add_event_callback(DoorbellButton, Button_callback)




GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(DoorbellRelay, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(AnotherRelay,  GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(DoorbellLed,   GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(DoorbellButton,GPIO.IN,  pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(DoorbellButton,   GPIO.FALLING, bouncetime=200)
GPIO.add_event_callback(DoorbellButton, Button_callback)


try:
    while(1):
        sleep(1)

except KeyboardInterrupt:
    print("Shutting down...")
    GPIO.remove_event_detect(DoorbellButton)
    GPIO.cleanup()


#
