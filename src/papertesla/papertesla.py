# -*- coding: utf-8 -*-

"""Main Module

PaperTesla Controller
"""

import ulogging as logging
from papertesla.comms import BLEController
from papertesla.led import LEDStrip


class PaperTesla:
    """PaperTesla Controller

    Primary acts as a mediator between
    bluetooth communication and LEDStrip instances.

    """
    COMMANDS = {}

    def __init__(self, ble):
        self._ble = BLEController(ble, name='PaperTesla')
        self._leds = set()
        self.log = logging.getLogger('papertesla')
        self.log.info("PaperTesla Booted!")
        self._ble.on_write = self._handle_write
        self._ble.advertise()

    def add_led(self, pin, name, led_n):
        """Add led strip"""
        strip = LEDStrip(pin, name, led_n)
        self.log.info('adding new LED strip: %s' % strip.name)
        if strip not in self._leds:
            self._leds.add(strip)
            return strip
        self.log.error('LED strip with name %s already exists!' % name)
        return None

    def get_led(self, name):
        """retrieve led instance"""
        try:
            led = next((i for i in self._leds if i.name == name))
        except StopIteration:
            self.log.error('led %s not found!' % name)
            return None
        self.log.info('retrieved led: %s' % name)
        return led

    def _parse_command(self, cmd_str):
        """Parse command string"""
        args = [p.lower() for p in cmd_str.split()]
        cmd = args.pop(0)
        return (cmd, args)

    def _handle_write(self, value):
        """Handle incomming commands"""
        self.log.debug("CMD RECV: %s" % value)
        cmd, args = self._parse_command(value)
        self.log.debug("CMD: %s -- ARGS: %s" % (cmd, ','.join(args)))
        handler = self.COMMANDS.get(cmd, None)
        if handler:
            return handler(*args)

    def command(self, command):
        """Decorator for adding commands to PaperTesla

        Args:
            command: command to add

        Example:
            >>> @papertesla.command('GET_COLOR')
                def handle_get_color(led_alias):
                    # retrieve color somehow
                    color = get_color_function(led_alias)
                    print('got color!')
                    print(color)
        """
        class Deco:
            def __init__(self, func):
                self.func = func
                cmd = command.strip().lower()
                PaperTesla.COMMANDS[cmd] = func

            def __call__(self):
                return self.func()
        return Deco
