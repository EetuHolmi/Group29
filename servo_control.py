import uasyncio as asyncio
import machine
import random

# === Constants ===
MIN_SERVO_ANGLE = 50
MAX_SERVO_ANGLE = 130

# Calculate 4 equally spaced positions (including min and max)
NUM_POSITIONS = 4
servo_positions = [
    MIN_SERVO_ANGLE + i * (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE) // (NUM_POSITIONS - 1)
    for i in range(NUM_POSITIONS)
]

# Configure the servo PWM pin (adjust if needed).
servo_pin = machine.Pin(18)
servo = machine.PWM(servo_pin)
servo.freq(50)  # Standard 50Hz (20ms period)

async def set_servo_angle(angle):
    """
    Set the servo to a specific angle (0 to 180 degrees).
    """
    angle = max(0, min(180, angle))
    pulse_ms = 1 + (angle / 180)
    duty = int((pulse_ms / 20) * 65535)
    servo.duty_u16(duty)
    print(f"Servo: Setting angle to {angle}° (pulse: {pulse_ms:.2f} ms, duty: {duty})")
    await asyncio.sleep(0.03)

async def move_servo_to_random_position(current):
    """
    Randomly choose one of the 4 preset positions (excluding current).
    """
    available_positions = [pos for pos in servo_positions if pos != current]
    target = random.choice(available_positions)
    print(f"Servo: Moving from {current}° to target {target}°")

    step = 2 if target > current else -2
    for angle in range(current, target + step, step):
        await set_servo_angle(angle)
        await asyncio.sleep(0.05)

    print(f"Servo: Reached {target}°")
    return target
