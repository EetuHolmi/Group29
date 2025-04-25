import machine
import time

# === Setup ===
motorPWM = machine.PWM(machine.Pin(17))
motorPWM.freq(1000)
motorCW = machine.Pin(14, machine.Pin.OUT)
motorACW = machine.Pin(15, machine.Pin.OUT)


def run_motor(speed, direction, run_time):
    """
    Run motor at given speed and direction for run_time seconds.
    direction: 'cw' (clockwise), 'acw' (anti-clockwise), 'stop'
    """
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
    time.sleep(run_time)
    # Stop motor after time
    motorCW.value(0)
    motorACW.value(0)
    motorPWM.duty_u16(0)
    print("Motor stopped")


if __name__ == '__main__':
    print("Motor Control Script")
    while True:
        run_motor(65535, 'cw', 5)
        time.sleep(1)

