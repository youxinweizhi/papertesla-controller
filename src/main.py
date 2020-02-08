# main.py

import bluetooth  # pylint: disable=import-error
from micropython import alloc_emergency_exception_buf
from papertesla.comms import BLEController

# Allocate RAM for exceptions
alloc_emergency_exception_buf(100)

blu = bluetooth.BLE()
controller = BLEController(blu)
