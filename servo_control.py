import machine
import random
import time

# === Constants ===
MIN_SERVO_ANGLE = 50
MAX_SERVO_ANGLE = 130

# Calculate 4 equally spaced positions (including min and max)
NUM_POSITIONS = 4
servo_positions = [
    MIN_SERVO_ANGLE + i * (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE) // (NUM_POSITIONS - 1)
    for i in range(NUM_POSITIONS)
]

# Configure the servo PWM pin
servo_pin = machine.Pin(18)
servo = machine.PWM(servo_pin)
servo.freq(50)  # Standard servo PWM frequency


def set_servo_angle(angle):
    """
    Sets servo angle (0–180) for SG90 using calibrated duty values.
    """
    angle = max(0, min(180, angle))
    
    # SG90: 0.5ms to 2.4ms pulse width (narrower than standard)
    min_duty = 1638   # 0.5 ms pulse (1638/65535 ≈ 2.5%)
    max_duty = 7864   # 2.4 ms pulse (7864/65535 ≈ 12%)

    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    print(f"SG90 angle: {angle}, duty: {duty}")
    time.sleep(0.3)


def move_servo_to_random_position(current):
    """
    Randomly choose one of the 4 preset positions (excluding current),
    and move to it smoothly.
    """
    available_positions = [pos for pos in servo_positions if pos != current]
    target = random.choice(available_positions)
    print(f"Servo: Moving from {current}° to {target}°")

    step = 2 if target > current else -2
    for angle in range(current, target + step, step):
        set_servo_angle(angle)
        time.sleep(0.05)

    print(f"Servo: Reached {target}°")
    return target


# === Example Usage ===
if __name__ == "__main__":
    current_angle = 90
    set_servo_angle(current_angle)
    current_angle = move_servo_to_random_position(current_angle)
