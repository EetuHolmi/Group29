import uasyncio as asyncio
import machine
import random
import wifi
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

# WiFi connect at the start
net = wifi.connect_or_create_ap()
print("Device IP:", net.ifconfig()[0])


async def blink_led():
    while True:
        led.value(1)
        await asyncio.sleep(1)
        led.value(0)
        await asyncio.sleep(1)


def random_number():
    return random.randint(1, 3)


async def game_loop():
    while True:
        sensor_value = ir_sensor_control.get_ir_value()
        if sensor_value == 0:
            print("Ball detected by IR sensor!")
            servo_control.move_servo_to_position(random.randint(1, 3))
            dc_motor_control.run_motor(65535, 'cw', 5)
        await asyncio.sleep(0.5)  # Check every half second


async def handle_client(reader, writer):
    request_line = await reader.readline()
    print("Request:", request_line)

    while await reader.readline() != b"\r\n":
        pass

    request = request_line.decode()
    if "GET /start" in request:
        print("Web: Start command received")
        servo_control.move_servo_to_start_position()
        sensor_value = ir_sensor_control.get_ir_value()
        if sensor_value == 0:
            servo_control.move_servo_to_position(random_number())
            dc_motor_control.run_motor(65535, 'cw', 5)

    response = """\
HTTP/1.1 200 OK

<html>
    <head><title>Control Panel</title></head>
    <body>
        <h1>Control Panel</h1>
        <form action="/start" method="get">
            <button type="submit">Start Game</button>
        </form>
    </body>
</html>
"""
    writer.write(response.encode())
    await writer.drain()
    await writer.wait_closed()


async def main():
    print("Let's Start The Game")
    asyncio.create_task(blink_led())
    # Move servo to start position
    servo_control.move_servo_to_start_position()
    # Start the game loop
    asyncio.create_task(game_loop())

    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Web server running...")

    # Keep alive manually
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
