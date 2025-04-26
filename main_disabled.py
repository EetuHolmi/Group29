import uasyncio as asyncio
import machine
import random
import ir_sensor_control
import servo_control
import dc_motor_control

# Setup
led = machine.Pin("LED", machine.Pin.OUT)
ir_sensor = machine.Pin(16, machine.Pin.IN)

# Motor
motorPWM = machine.PWM(machine.Pin(17))
motorPWM.freq(1000)
motorCW = machine.Pin(14, machine.Pin.OUT)
motorACW = machine.Pin(15, machine.Pin.OUT)


async def blink_led():
    while True:
        led.value(1)
        await asyncio.sleep(1)
        led.value(0)
        await asyncio.sleep(1)


def random_number():
    return random.randint(1, 3)


async def main():
    print("Let's Start The Game")
    asyncio.create_task(blink_led())
    # Move servo to start position
    servo_control.move_servo_to_start_position()

    while True:
        await asyncio.sleep(1)
        # Check IR sensor value
        sensor_value = ir_sensor_control.get_ir_value()
        if sensor_value == 0:
            print(f"IR Sensor Value: {sensor_value}")
            # Move servo to position 1
            servo_control.move_servo_to_position(random_number())
            # Run motor clockwise for 5 seconds
            dc_motor_control.run_motor(65535, 'cw', 5)


asyncio.run(main())
