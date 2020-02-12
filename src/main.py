# main.py

import bluetooth  # pylint: disable=import-error
import ulogging as logging
from micropython import alloc_emergency_exception_buf
from papertesla import PaperTesla

# Allocate RAM for exceptions
alloc_emergency_exception_buf(100)

# Logging Config
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('main')

# Setup
blu = bluetooth.BLE()
papertesla = PaperTesla(blu)

# Add LED strip
papertesla.add_led(21, 'main', 50)


@papertesla.command('SET_COLOR')
def handle_set_color(led_alias, color):
    """Set LED strip to given color.

    >>> SET_COLOR <LED_ALIAS> <COLOR>

    Args:
        led_alias: alias of LED strip
        color: color to set.

    Example:
        >>> SET_COLOR main red4
        >>> SET_COLOR headlight1 whitesmoke
    """
    log.info('setting color: %s' % color)
    led = papertesla.get_led(led_alias)
    led.color = color
