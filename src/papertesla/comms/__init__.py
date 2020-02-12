# -*- coding: utf-8 -*-

"""Communications Module

PaperTesla Controller
"""

import array
import struct

import bluetooth  # pylint: disable=import-error
import ulogging as logging
from ucollections import namedtuple

from . import advertise
from . import constants as C

# Read/Write Handler
RWHandler = namedtuple("RWHandler", ("rx", "tx"))


class BLEController:
    UART_SERVICE = (C.UART_UUID,
                    (C.UART_RX, C.UART_TX),)

    def __init__(self, ble, name='PaperTesla'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(handler=self._irq_handler)
        self._connections = set()
        self.name = name
        self.log = logging.getLogger('BLECtrl')
        self._handler = self._register_services()
        self._buffer = bytearray()
        self._payload = None
        self.on_connect = None
        self.on_disconnect = None

    @property
    def ble(self):
        """bluetooth singleton"""
        return self._ble

    def _register_services(self):
        """register GATTS services"""
        self.log.debug('registering GATTS services...')
        services = (self.UART_SERVICE, )
        ((rx, tx, ),) = self._ble.gatts_register_services(services)
        handler = RWHandler(rx, tx)
        self._ble.gatts_set_buffer(handler.rx, C.RX_BUFFER, True)
        return handler

    def _irq_handler(self, event, data):
        """Interrupt Handler"""
        if event == C.IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self.log.info("new device connected")
            if self.on_connect:
                return self.on_connect(conn_handle)
        if event == C.IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self.log.info("connection lost!")
            if self.on_disconnect:
                self.on_disconnect(conn_handle)
            return self.advertise()
        if event == C.IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            self.log.info("incoming data...")
            if conn_handle in self._connections and value_handle == self._handler.rx:
                incom_data = self._ble.gatts_read(self._handler.rx)
                self.log.debug("data: %s" % incom_data)
                self._buffer += incom_data
                self.log.info("saved to buffer!")
        return None

    def advertise(self, interval_us=500000):
        """begin GATTS advertising"""
        self.log.info("starting GATTS advertising...")
        if not self._payload:
            self._payload = advertise.advertising_payload(
                name=self.name, appearance=C.CHAR_APP_GENERIC_REMOTE)
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        self.log.info("now advertising!")
        return True

    def read(self, sz=None):
        """read data from rx buffer"""
        if not sz:
            sz = len(self._buffer)
        result = self._buffer[0:sz]
        self._buffer = self._buffer[sz:]
        return result

    def write(self, data):
        """write data to tx char"""
        for conn in self._connections:
            self._ble.gatts_notify(conn, self._handler.tx, data)

    def parse(self):
        """read from buffer and convert to string"""
        data = self.read()
        parsed = data.decode().strip()
        self.log.info('parsed data: %s' % parsed)
        return parsed
