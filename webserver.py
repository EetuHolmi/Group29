import socket
import time
import uasyncio as asyncio
from servo_control import set_servo_angle

def serve_web(motorPWM, motorCW, motorACW):
    current_angle = 90

    def run_motor_web(speed=65535, direction="cw", duration=3):
        if direction == "cw":
            motorCW.value(1)
            motorACW.value(0)
        elif direction == "acw":
            motorCW.value(0)
            motorACW.value(1)
        else:
            motorCW.value(0)
            motorACW.value(0)
        motorPWM.duty_u16(speed)
        time.sleep(duration)
        motorCW.value(0)
        motorACW.value(0)
        motorPWM.duty_u16(0)

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server running at 192.168.4.1")

    while True:
        try:
            cl, addr = s.accept()
            print("Client connected:", addr)
            req = cl.recv(1024).decode()

            angle = current_angle
            run_motor = False

            if "GET /set?" in req:
                try:
                    query = req.split("/set?")[1].split(" ")[0]
                    params = query.split("&")
                    for p in params:
                        if p.startswith("servo="):
                            angle = int(p.split("=")[1])
                            current_angle = angle
                            asyncio.run(set_servo_angle(angle))
                        elif p == "motor=start":
                            run_motor = True
                    if run_motor:
                        run_motor_web()
                except Exception as e:
                    print("Request parse error:", e)

            html = f"""HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<!DOCTYPE html>
<html>
<head>
  <title>PingPong Bot</title>
  <style>
    body {{ font-family: Arial; text-align: center; padding: 20px; }}
    input[type=range] {{ width: 80%; }}
    button {{ font-size: 18px; padding: 10px 20px; }}
  </style>
</head>
<body>
  <h2>Servo Angle: <span id="angleVal">{angle}</span>°</h2>
  <form action="/set">
    <input type="range" min="0" max="180" value="{angle}" name="servo" id="servoSlider" oninput="angleVal.innerText=this.value">
    <br><br>
    <button type="submit" name="motor" value="start">Start Motor</button>
  </form>
</body>
</html>
"""

            try:
                cl.send(html.encode())
            except Exception as e:
                print("Send error:", e)

            cl.close()
        except Exception as e:
            print("Socket error:", e)
