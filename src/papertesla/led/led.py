# -*- coding: utf-8 -*-

"""LED Strip Segement Abstractions"""

import neopixel
import ulogging as logging
from machine import Pin

from .color import COLORS


class LEDStrip:
    """LED Strip Abstraction"""

    def __init__(self, pin, name, led_n, init_color='whitesmoke'):
        self._pin = Pin(pin, Pin.OUT)
        self._name = name
        self._np = neopixel.NeoPixel(self._pin, led_n)
        self.log = logging.getLogger(self._name)
        self.log.debug('init LED strip: %s' % self._name)
        self._color = COLORS[init_color]

    @property
    def pin(self):
        """LED Strip Pin"""
        return self._pin

    @property
    def name(self):
        """LED Strip Alias"""
        return self._name

    @property
    def color(self):
        """Current color value"""
        return self._color

    @color.setter
    def color(self, value):
        """Set current color"""
        self._color = COLORS[value]
        return self._fill_color(self._color)

    def _fill_color(self, color):
        """Set all leds to color"""
        self._np.fill(color)
        self._np.write()
        return color

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, value):
        return self.name == value
