import uasyncio as asyncio
import machine
import time
import wifi
import _thread
from webserver import serve_web
from servo_control import random_servo_move, set_servo_angle

# Setup
led = machine.Pin("LED", machine.Pin.OUT)
ir_sensor = machine.Pin(16, machine.Pin.IN)

# Motor
motorPWM = machine.PWM(machine.Pin(17))
motorPWM.freq(1000)
motorCW = machine.Pin(14, machine.Pin.OUT)
motorACW = machine.Pin(15, machine.Pin.OUT)

# Connect to WiFi or fallback to AP
net = wifi.connect_or_create_ap()

# Start webserver thread only once
if not globals().get("_web_thread_started", False):
    _thread.start_new_thread(serve_web, (motorPWM, motorCW, motorACW))
    globals()["_web_thread_started"] = True

# Show IP
print("Device IP:", net.ifconfig()[0])

async def blink_led():
    while True:
        led.value(1)
        await asyncio.sleep(1)
        led.value(0)
        await asyncio.sleep(1)

async def get_ir_sensor_value():
    val = ir_sensor.value()
    #print("IR Sensor:", "Ball detected" if val == 0 else "Not detected")
    return val

async def run_motor(speed, direction, run_time):
    if direction == 'cw':
        motorCW.value(1)
        motorACW.value(0)
    elif direction == 'acw':
        motorCW.value(0)
        motorACW.value(1)
    else:
        motorCW.value(0)
        motorACW.value(0)

    motorPWM.duty_u16(speed if direction != 'stop' else 0)
    print(f"Motor: {direction} at speed {speed} for {run_time}s")
    await asyncio.sleep(run_time)
    motorCW.value(0)
    motorACW.value(0)
    motorPWM.duty_u16(0)

async def main():
    asyncio.create_task(blink_led())
    current_servo = 90
    await set_servo_angle(current_servo)
    last_ball_ms = time.ticks_ms()

    while True:
        sensor_val = await get_ir_sensor_value()
        if sensor_val == 0:
            last_ball_ms = time.ticks_ms()
            await run_motor(65535, 'cw', 2.9)
            current_servo = await random_servo_move(current_servo, 50, 130, step=2, delay=0.03)
            await asyncio.sleep(4)
        else:
            if time.ticks_diff(time.ticks_ms(), last_ball_ms) > 10000:
                if current_servo != 90:
                    print("No ball for 10s. Re-centering servo.")
                    await set_servo_angle(90)
                    current_servo = 90
            else:
                print(f"No ball, servo holds at {current_servo}°")
            await asyncio.sleep(0.5)
        await asyncio.sleep(0.1)

asyncio.run(main())
