import uasyncio as asyncio
import machine
import random

# Configure the servo PWM pin (adjust if needed).
servo_pin = machine.Pin(18)
servo = machine.PWM(servo_pin)
servo.freq(50)  # Standard 50Hz (20ms period) for most hobby servos.

async def set_servo_angle(angle):
    """
    Set the servo to a specific angle (0 to 180 degrees).
    The pulse width is approximated so that 0° ≈ 1ms and 180° ≈ 2ms.
    """
    # Clamp the angle.
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # Calculate the pulse width: 0° -> ~1ms, 180° -> ~2ms.
    pulse_ms = 1 + (angle / 180)
    # For a 20ms period (50Hz), convert pulse width to a 16-bit duty cycle.
    duty = int((pulse_ms / 20) * 65535)
    servo.duty_u16(duty)
    print("Servo: Setting angle to {}° (pulse: {:.2f} ms, duty: {})".format(angle, pulse_ms, duty))
    await asyncio.sleep(0.01)

async def random_servo_move(current, min_angle, max_angle, step=2, delay=0.03):
    """
    Moves the servo from its current angle to a random target between min_angle and max_angle.
    Returns the new angle.
    """
    target = random.randint(min_angle, max_angle)
    print("Servo: Moving from {}° to new target {}°".format(current, target))
    # Determine the direction (increasing or decreasing) and create a range.
    if current < target:
        angle_range = range(current, target + 1, step)
    else:
        angle_range = range(current, target - 1, -step)
    
    for angle in angle_range:
        await set_servo_angle(angle)
        await asyncio.sleep(delay)
        
    print("Servo: Reached target {}°".format(target))
    return target
