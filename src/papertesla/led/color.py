# -*- coding: utf-8 -*-

"""LED Color Helpers and Definitions"""

from ucollections import OrderedDict, namedtuple

Color = namedtuple('RGB', ('red', 'green', 'blue'))

COLORS = {}


class RGB(Color):
    """RGB Color Abstraction"""

    def to_hex(self):
        """convert color to hex"""
        return '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)


# Colors
WHITESMOKE = RGB(245, 245, 245)
ORANGE = RGB(255, 128, 0)
RED4 = RGB(139, 0, 0)

COLORS['whitesmoke'] = WHITESMOKE
COLORS['orange'] = ORANGE
COLORS['red4'] = RED4


COLORS = OrderedDict(sorted(COLORS.items()), key=lambda x: x[0])
