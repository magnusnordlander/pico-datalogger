# Test and Demo code for Maker Pi Pico
# Reference: https://my.cytron.io/p-maker-pi-pico
# Installing CircuitPython - https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
# Audio track credit: jeremy80 - L-R Tone Level Test @ -6 db max w/3 Sec. Countdown Leader
# Audio track reference: https://freesound.org/people/jeremy80/sounds/230639/

################################################################################
# Scan for available WiFi AP, connect to the speicifed AP and ping 8.8.8.8.
# This is modified from Adafruit's esp_atcontrol_simpletest.py.
#
# Hardware:
# - Maker Pi Pico or Maker Pi RP2040
# - ESP8266 WiFi module with Espressif AT Firmware v2.2.0 and above.
#
# Dependencies:
# - adafruit_requests
# - adafruit_espatcontrol
#
# Instructions:
# - Copy the lib folder to the CIRCUITPY device.
# - Modify the keys in secrets.py and copy to the CIRCUITPY device.
# - Make sure the UART pins are defined correctly according to your hardware.
#
#
# Author: Cytron Technologies
# Website: www.cytron.io
# Email: support@cytron.io
################################################################################

import time
import board
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol

secrets = {
    "ssid"                     : "IoT Transform",                                    
    "password"                 : "",
    "blynk_auth_token"         : "my_blynk_auth_token",
    "thingspeak_write_api_key" : "my_thingspeak_write_api_key",
    "telegram_bot_token"       : "my_telegram_bot_token",
    "telegram_chat_id"         : "my_telegram_chat_id",
    "aio_username"             : "my_adafruitio_username",
    "aio_key"                  : "my_adafruitio_key"
}

# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
requests.set_socket(socket, esp)

print("Resetting ESP module")
esp.soft_reset()

first_pass = True
while True:
    try:
        if first_pass:
            print("\nScanning for WiFi AP...")
            for ap in esp.scan_APs():
                print(ap)
                
            print("\nConnecting...")
            esp.connect(secrets)
            print("IP address:", esp.local_ip)
            print("ESP Firmware Version:", esp.version)
            print()
            first_pass = False
            
        print("Pinging 8.8.8.8...", end="")
        print(esp.ping("8.8.8.8"))
        time.sleep(10)
        
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)
