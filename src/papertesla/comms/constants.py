# -*- coding: utf-8 -*-

"""Communication related Constants

PaperTesla Controller
"""

import bluetooth  # pylint: disable=import-error
from micropython import const

# ---- GATT ----

# Nordic UART (Serial over BLE)
UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'),
           bluetooth.FLAG_NOTIFY,)
UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'),
           bluetooth.FLAG_WRITE,)
EOT = bytearray('EOT')

# org.bluetooth.characteristic.gap.appearance.xml
#: generic remote control
CHAR_APP_GENERIC_REMOTE = const(384)


# ---- IRQ Events ----

IRQ_CENTRAL_CONNECT = const(1 << 0)
IRQ_CENTRAL_DISCONNECT = const(1 << 1)
IRQ_GATTS_WRITE = const(1 << 2)

# ---- Config ----
RX_BUFFER = 100
