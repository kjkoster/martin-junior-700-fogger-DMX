import threading
import time
import datetime
import RPi.GPIO as GPIO
from roh.dmx.client.dmx_client import DmxClient
from roh.dmx.client.dmx_client_callback import DmxClientCallback
from typing import Dict

RELAY_GPIO_PIN = 25

DMX_DEVICE = "/dev/ttyAMA0"
DMX_CHANNELS = [510, 511, 512]

status = False
stamp = datetime.datetime.now()

on_off = False
sec_on = 0
sec_off = 0

def thread_function():
    global status
    global on_off
    global sec_on
    global sec_off
    global stamp

    while True:
        if on_off:
            new_status = status
            if sec_on == 0 and sec_off == 0:
                new_status = True
            elif status:
                if datetime.datetime.now() > stamp + datetime.timedelta(seconds=sec_on):
                    new_status = False
            else:
                if datetime.datetime.now() > stamp + datetime.timedelta(seconds=sec_off):
                    new_status = True
        else:
            new_status = False

        if status != new_status:
            status = new_status
            stamp = datetime.datetime.now()

        GPIO.output(RELAY_GPIO_PIN, status)

        print(f"{datetime.datetime.now()} status {status} on_off {on_off} sec_on {sec_on} sec_off {sec_off}")
        time.sleep(0.1)

class MyDmxCallback(DmxClientCallback):
    """
    Example implementation of all available callback methods
    """
    def sync_lost(self) -> None:
        print("sync lost")

    def sync_found(self) -> None:
        print("sync found")

    def data_received(self, monitored_data: Dict[int, int]) -> None:
        global on_off
        global sec_on
        global sec_off

        print(f"valid monitored data: {monitored_data}")

        on_off = monitored_data[510] > 127
        sec_on = monitored_data[511]
        sec_off = monitored_data[512]

        print(f"    on_off: {on_off}, sec_on: {sec_on}, sec_off: {sec_off}")

    def full_data_received(self, data: bytes) -> None:
        pass

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)
    print(f"{datetime.datetime.now()} starting relay control thread using GPIO BCM pin {RELAY_GPIO_PIN}")
    x = threading.Thread(target=thread_function)
    x.start()

    print(f"{datetime.datetime.now()} starting DMX client on {DMX_DEVICE}, listening on channels {DMX_CHANNELS}")
    c: DmxClient = DmxClient(DMX_DEVICE, DMX_CHANNELS, MyDmxCallback())
    c.run()

    x.join()
    print("Main    : all done")

