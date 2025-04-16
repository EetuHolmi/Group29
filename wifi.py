import network
import time

def connect_or_create_ap(ssid="PingPongBot", password="12345678", wifi_ssid="Loading...", wifi_pass="hahahahaha"):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_pass)

    print("Trying to connect to WiFi...")
    for _ in range(10):
        if wlan.isconnected():
            print("Connected to WiFi:", wlan.ifconfig()[0])
            return wlan
        time.sleep(0.5)

    print("WiFi failed. Creating Access Point...")
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while not ap.active():
        pass

    print("Access Point started:", ap.ifconfig()[0])
    return ap

