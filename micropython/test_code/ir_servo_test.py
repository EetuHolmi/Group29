from machine import Pin, PWM
import utime

# define led and ir_sensor pins

ir_sensor = Pin(16, Pin.IN)

#define servo positions
MID = 1500000
MIN = 1000000
MAX = 1800000

#flag to see if servo in use
servo_running = False

#define servo pin
servo = PWM(Pin(15))
servo.freq(50)
servo.duty_ns(MID)

# function to rotate servo between 3 positions 
def use_servo():
    global servo_running
    servo_running = True
    
    servo.duty_ns(MIN)
    utime.sleep(1)
    servo.duty_ns(MID)
    utime.sleep(1)
    servo.duty_ns(MAX)
    utime.sleep(2)
    
    
    servo_running = False
    
    

# infinite loop to check sensor and change led and run servo if something detected
while True:
    
    #print(ir_sensor.value())
    
    # if something detected
    if ir_sensor.value() == 0:

        print(servo_running)
        if not servo_running:
            use_servo()
            
    else:
        pass
        
    utime.sleep(0.1)
    
