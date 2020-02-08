# -*- coding: utf-8 -*-

"""Communication related Constants

PaperTesla Controller
"""

import bluetooth  # pylint: disable=import-error
from micropython import const

# ---- GATT Services ----

# org.bluetooth.service.generic_access
SERV_GENERIC_ACCESS = bluetooth.UUID(0x1800)


# ---- GATT Chars ----

# org.bluetooth.characteristic.digital_output
CHAR_DIGIO_RX = (bluetooth.UUID(0x2A57),
                 bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
CHAR_DIGIO_TX = (bluetooth.UUID(0x2A57),
                 bluetooth.FLAG_WRITE,)

# org.bluetooth.characteristic.gap.appearance.xml
#: generic remote control
CHAR_APP_GENERIC_REMOTE = const(384)

# ---- IRQ Events ----

IRQ_CENTRAL_CONNECT = const(1 << 0)
IRQ_CENTRAL_DISCONNECT = const(1 << 1)

