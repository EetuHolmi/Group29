import uasyncio as asyncio
import machine
import random

import screen
import wifi
import ir_sensor_control
import servo_control
import dc_motor_control

game_running = False
motor_run_time = 5  # default seconds

# Setup
led = machine.Pin("LED", machine.Pin.OUT)
ir_sensor = machine.Pin(16, machine.Pin.IN)

# Motor
motorPWM = machine.PWM(machine.Pin(17))
motorPWM.freq(1000)
motorCW = machine.Pin(14, machine.Pin.OUT)
motorACW = machine.Pin(15, machine.Pin.OUT)

# WiFi connect
net = wifi.connect_or_create_ap()
ip_address = net.ifconfig()[0]
print("Device IP:", ip_address)

# Show IP on the OLED
screen.update_display(ip_address, "Waiting...", "")


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
                screen.update_display(ip_address, "Ball Detected!", "Throwing...")
                servo_control.move_servo_to_position(random.randint(1, 3))
                await dc_motor_control.run_motor(65535, 'cw', motor_run_time)
                await asyncio.sleep(0)
        await asyncio.sleep(0.5)


async def handle_client(reader, writer):
    global game_running, motor_run_time

    try:
        request_line = await reader.readline()
        print("Request:", request_line)

        while await reader.readline() != b"\r\n":
            pass

        request = request_line.decode()

    except Exception as e:
        print("Error reading request:", e)
        await writer.wait_closed()
        return

    if "favicon.ico" in request:
        writer.write("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        await asyncio.sleep(0.001)
        return

    if "GET /start_auto" in request:
        game_running = True
        screen.update_display(ip_address, "Auto Mode", "Running...")
    elif "GET /stop_auto" in request:
        game_running = False
        screen.update_display(ip_address, "Manual Mode", "Stopped")
    elif "GET /manual_pos1" in request:
        servo_control.move_servo_to_position(1)
        screen.update_display(ip_address, "Manual Move", "Position 1")
        await asyncio.sleep(0)
    elif "GET /manual_pos2" in request:
        servo_control.move_servo_to_position(2)
        screen.update_display(ip_address, "Manual Move", "Position 2")
        await asyncio.sleep(0)
    elif "GET /manual_pos3" in request:
        servo_control.move_servo_to_position(3)
        screen.update_display(ip_address, "Manual Move", "Position 3")
        await asyncio.sleep(0)
    elif "GET /throw" in request:
        await dc_motor_control.run_motor(65535, 'cw', motor_run_time)
        screen.update_display(ip_address, "Manual Throw", "")
        await asyncio.sleep(0)
    elif "GET /set_motor_time" in request:
        if "time=" in request:
            try:
                selected = int(request.split("time=")[1].split()[0].split("&")[0])
                if 5 <= selected <= 15:
                    motor_run_time = selected
                    print(f"Motor run time set to {motor_run_time} seconds")
                    screen.update_display(ip_address, "Motor Time Set", f"{motor_run_time}s")
                redirect_response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
                writer.write(redirect_response.encode())
                await writer.drain()
                await writer.wait_closed()
                return
            except Exception as e:
                print("Error parsing motor time:", e)

    selected_5 = "selected" if motor_run_time == 5 else ""
    selected_6 = "selected" if motor_run_time == 6 else ""
    selected_7 = "selected" if motor_run_time == 7 else ""
    selected_8 = "selected" if motor_run_time == 8 else ""
    selected_9 = "selected" if motor_run_time == 9 else ""
    selected_10 = "selected" if motor_run_time == 10 else ""
    selected_11 = "selected" if motor_run_time == 11 else ""
    selected_12 = "selected" if motor_run_time == 12 else ""
    selected_13 = "selected" if motor_run_time == 13 else ""
    selected_14 = "selected" if motor_run_time == 14 else ""
    selected_15 = "selected" if motor_run_time == 15 else ""

    if game_running:
        auto_button_text = "Stop Automatic Game"
        auto_button_action = "/stop_auto"
        auto_status = "Status: Auto Mode Running"
    else:
        auto_button_text = "Start Automatic Game"
        auto_button_action = "/start_auto"
        auto_status = "Status: Manual Mode"

    response = f"""HTTP/1.1 200 OK

<html>
<head>
<title>Ping Pong Bot Control</title>
<style>
body {{
    text-align: center;
    font-family: Arial, sans-serif;
    margin-top: 30px;
}}

button {{
    padding: 15px 25px;
    font-size: 18px;
    margin: 10px;
    border-radius: 8px;
    background-color: #4CAF50;
    color: white;
    border: none;
}}

button:hover {{
    background-color: #45a049;
}}

select {{
    padding: 10px;
    font-size: 16px;
    margin: 10px;
    border-radius: 5px;
}}

h1 {{
    color: #333;
}}
</style>
</head>

<body>

<h1>Motor Time Setting</h1>
<form action="/set_motor_time" method="get">
    <label for="time">Motor Run Time (seconds):</label><br>
    <select name="time">
        <option value="5" {selected_5}>5</option>
        <option value="6" {selected_6}>6</option>
        <option value="7" {selected_7}>7</option>
        <option value="8" {selected_8}>8</option>
        <option value="9" {selected_9}>9</option>
        <option value="10" {selected_10}>10</option>
        <option value="11" {selected_11}>11</option>
        <option value="12" {selected_12}>12</option>
        <option value="13" {selected_13}>13</option>
        <option value="14" {selected_14}>14</option>
        <option value="15" {selected_15}>15</option>
    </select><br><br>
    <button type="submit">Set Motor Time</button>
</form>

<h1>Manual Control</h1>
<button onclick="sendRequest('/manual_pos1')">Move Servo to Position 1</button><br><br>
<button onclick="sendRequest('/manual_pos2')">Move Servo to Position 2</button><br><br>
<button onclick="sendRequest('/manual_pos3')">Move Servo to Position 3</button><br><br>
<button onclick="sendRequest('/throw')">Throw Ball (Start Motor)</button><br><br>

<h1>Automatic Control</h1>
<button onclick="sendRequest('{auto_button_action}')">{auto_button_text}</button><br><br>

<h2>{auto_status}</h2>

<script>
function sendRequest(path) {{
    fetch(path)
    .then(response => {{
        console.log("Request sent:", path);
        setTimeout(() => location.reload(), 1000); // 1 second reload
    }})
    .catch(error => console.error('Error:', error));
}}
</script>

</body>
</html>
"""
    writer.write(response.encode())
    await writer.drain()
    await writer.wait_closed()


async def main():
    print("Let's Start The Game")
    screen.update_display(ip_address, "Game Ready", "")
    asyncio.create_task(blink_led())
    servo_control.move_servo_to_start_position()
    asyncio.create_task(game_loop())
    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Web server running...")

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
