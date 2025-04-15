from machine import Pin, PWM
import utime

# define led and ir_sensor pins
led = Pin(16, Pin.OUT)
ir_sensor = Pin(15, Pin.IN)


#flag to see if servo in use
servo_running = False

# uses the motor with speed (0-100), on_off indicates if
# motor to be turned on or off
def use_motor(speed, on_off):
    #reserve flag
    global servo_running
    servo_running = True
    
    speed = min(100, speed)
    speed = max(0, speed)
    
    #connector to Hbridge EN1,2
    Speed = PWM(Pin(14))
    Speed.freq(50)
    
    #connector to hbridge A1
    cw = Pin(17, Pin.OUT)
    
    #set speed
    Speed.duty_u16(int(speed/100*65536))
    
    #set on or off
    if on_off:
        cw.value(1)
    else:
        cw.value(0)
    
    #free flag
    servo_running = False

# function to rotate servo between 3 positions     
    

# infinite loop to check sensor and change led and run motor if something detected
while True:
    
    #print(ir_sensor.value())
    
    # if something detected
    if ir_sensor.value() == 0:
        led.value(1)
        #print(servo_running)
        if not servo_running:
            #use_servo()
            #motor on
            use_motor(100, True)
            #wait 3 sec
            utime.sleep(3)
            #motor off
            use_motor(50, False)
    else:
        # what happens at neutral when nothing detected,
        # currently turns of the led
        led.value(0)
        
    utime.sleep(0.1)
    

