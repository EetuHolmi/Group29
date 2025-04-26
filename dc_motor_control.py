import uasyncio as asyncio
import machine

motorPWM = machine.PWM(machine.Pin(17))
motorPWM.freq(1000)
motorCW = machine.Pin(14, machine.Pin.OUT)
motorACW = machine.Pin(15, machine.Pin.OUT)

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
    print(f"Motor running {direction} at speed {speed} for {run_time} seconds")

    await asyncio.sleep(run_time)

    motorCW.value(0)
    motorACW.value(0)
    motorPWM.duty_u16(0)
    print("Motor stopped")
