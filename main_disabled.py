import uasyncio as asyncio
import machine
import random
import wifi
import ir_sensor_control
import servo_control
import dc_motor_control

game_running = False

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
        if game_running:
            sensor_value = ir_sensor_control.get_ir_value()
            if sensor_value == 0:
                print("Ball detected by IR sensor!")
                servo_control.move_servo_to_position(random.randint(1, 3))
                dc_motor_control.run_motor(65535, 'cw', 5)

        await asyncio.sleep(0.5)  # Check every half second


# Global variable to track if game loop is running
game_task = None


async def handle_client(reader, writer):
    global game_running

    request_line = await reader.readline()
    print("Request:", request_line)

    while await reader.readline() != b"\r\n":
        pass

    request = request_line.decode()

    if "favicon.ico" in request:
        writer.write("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        await writer.drain()
        await writer.wait_closed()
        return

    # === Handle Web Commands ===
    if "GET /start_auto" in request:
        print("Start auto mode")
        game_running = True
    elif "GET /stop_auto" in request:
        print("Stop auto mode")
        game_running = False
    elif "GET /manual_pos1" in request:
        print("Move servo to Position 1")
        servo_control.move_servo_to_position(1)
    elif "GET /manual_pos2" in request:
        print("Move servo to Position 2")
        servo_control.move_servo_to_position(2)
    elif "GET /manual_pos3" in request:
        print("Move servo to Position 3")
        servo_control.move_servo_to_position(3)
    elif "GET /throw" in request:
        print("Start motor to throw ball")
        dc_motor_control.run_motor(65535, 'cw', 5)

    # === Dynamic Button HTML ===
    if game_running:
        auto_button_text = "Stop Automatic Game"
        auto_button_action = "/stop_auto"
        auto_status = "Status: Auto Mode Running"
    else:
        auto_button_text = "Start Automatic Game"
        auto_button_action = "/start_auto"
        auto_status = "Status: Manual Mode"

    response = f"""\
HTTP/1.1 200 OK

<html>
<head>
    <title>Ping Pong Bot Control</title>
</head>
<body>
    <h1>Manual Control</h1>

    <form action="/manual_pos1" method="get">
        <button type="submit">Move Servo to Position 1</button>
    </form><br>

    <form action="/manual_pos2" method="get">
        <button type="submit">Move Servo to Position 2</button>
    </form><br>

    <form action="/manual_pos3" method="get">
        <button type="submit">Move Servo to Position 3</button>
    </form><br>

    <form action="/throw" method="get">
        <button type="submit">Throw Ball (Start Motor)</button>
    </form><br>

    <h1>Automatic Control</h1>
    <form action="{auto_button_action}" method="get">
        <button type="submit">{auto_button_text}</button>
    </form><br>

    <h2>{auto_status}</h2>

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
    game_task = asyncio.create_task(game_loop())
    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Web server running...")

    # Keep alive manually
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
