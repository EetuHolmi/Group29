import machine
import uasyncio as asyncio  # use asyncio instead of time

# === Constants ===
SERVO_START_POSITION = 90  # Main center position
SERVO_POSITIONS = {
    1: 60,  # Position 1
    2: 90,  # Position 2 (center)
    3: 120  # Position 3
}

# Configure the servo PWM pin
servo_pin = machine.Pin(18)
servo = machine.PWM(servo_pin)
servo.freq(50)  # Standard servo PWM frequency


async def set_servo_angle(angle, release_pwm=True):
    """
    Sets servo angle (0–180) for SG90.
    Optionally stop PWM after moving to reduce humming.
    """
    angle = max(0, min(180, angle))
    min_duty = 1638
    max_duty = 7864

    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    print(f"SG90 angle: {angle}, duty: {duty}")
    await asyncio.sleep(0.5)  # async wait for servo to move

    if release_pwm:
        servo.duty_u16(0)  # Stop PWM signal
        print("PWM released to reduce humming")


async def move_servo_to_position(position_number):
    """
    Move the servo to a predefined position: 1, 2, or 3.
    """
    if position_number not in SERVO_POSITIONS:
        print(f"Invalid position {position_number}")
        return

    target_angle = SERVO_POSITIONS[position_number]
    print(f"Moving to position {position_number} ({target_angle}°)")
    await set_servo_angle(target_angle)


async def move_servo_to_start_position():
    """
    Move the servo to its main start position.
    """
    print(f"Moving to start position ({SERVO_START_POSITION}°)")
    await set_servo_angle(SERVO_START_POSITION)


# === Example Usage (for testing directly) ===
if __name__ == "__main__":
    async def test():
        await move_servo_to_start_position()
        await asyncio.sleep(1)
        await move_servo_to_position(1)
        await asyncio.sleep(1)
        await move_servo_to_position(3)
        await asyncio.sleep(1)
        await move_servo_to_start_position()

    asyncio.run(test())
