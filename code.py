import random
import time

import adafruit_sdcard
import board
import busio
import digitalio
import microcontroller
import storage
import rtc
import time

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.GP4, board.GP5, baudrate=115200)

write_buffer = []

def init_system():
    r = rtc.RTC()
    r.datetime = time.struct_time((2019, 5, 29, 15, 14, 15, 0, -1, -1))

    # Connect to the card and mount the filesystem.
    spi = busio.SPI(board.GP10, board.GP11, board.GP12)
    cs = digitalio.DigitalInOut(board.GP15)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

def fill_buffer(next_fill):
    if time.monotonic() >= next_fill:
        t = microcontroller.cpu.temperature
        current_time = time.time()
        s = "%d: %0.1f" % (current_time, t)
        write_buffer.append(s)

        return next_fill + random.randint(0, 5)
    return next_fill

def write_out_buffer(next_writeout):
    if time.monotonic() >= next_writeout:
        if len(write_buffer) > 0:
            with open("/sd/temperature.txt", "a") as f:
                led.value = True  # turn on LED to indicate we're writing to the file
                print("Writing out")

                while len(write_buffer) > 0:
                    s = write_buffer.pop(0)
                    print(s)
                    f.write(s + "\n")

                led.value = False  # turn off LED to indicate we're done
                return next_writeout + random.randint(0, 10)
        else:
            print("Nothing to write out")
    return next_writeout

def main():
    next_fill = time.monotonic() + random.randint(0, 5)
    next_writeout = time.monotonic() + random.randint(0, 10)

    print("Logging temperature to filesystem")
    # append to the file!
    while True:
        next_fill = fill_buffer(next_fill)
        next_writeout = write_out_buffer(next_writeout)
        time.sleep(1)

def print_file():
    with open("/sd/temperature.txt", "r") as f:
        lines = f.readlines()
        print("Printing lines in file:")
        for line in lines:
            print(line)

init_system()
main()