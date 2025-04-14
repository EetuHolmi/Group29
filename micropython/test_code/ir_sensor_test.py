from machine import Pin
import utime

# define led and ir_sensor pins
led = Pin(16, Pin.OUT)
ir_sensor = Pin(15, Pin.IN)

# infinite loop to check sensor and change led
while True:
    print(ir_sensor.value())
    if ir_sensor.value() == 1:
        led.value(0)
    else:
        led.value(1) 



