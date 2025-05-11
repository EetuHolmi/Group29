import machine
import time

# === Setup ===
ir_sensor = machine.Pin(16, machine.Pin.IN)


def get_ir_value():
    sensor_val = ir_sensor.value()
    if sensor_val == 0:
        print("Object detected")
    else:
        print("No object detected")
    return sensor_val


if __name__ == '__main__':
    # This block will only run if the script is executed directly
    print("IR Sensor Control Script")
    while True:
        # Continuously check the IR sensor value
        sensor_value = get_ir_value()
        print(f"IR Sensor Value: {sensor_value}")
        time.sleep(0.2)