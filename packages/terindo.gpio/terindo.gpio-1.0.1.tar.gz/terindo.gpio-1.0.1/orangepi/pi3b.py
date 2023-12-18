# -*- coding: utf-8 -*-
# Copyright (c) 2023 terindo

"""
******** Warning Developement ********
** dont use this file in production **

Alternative pin mappings for Orange PI 3B
(Provide any additional details or source link here if needed)

Usage:

.. code:: python
   import orangepi.3b
   from OPi import GPIO

   GPIO.setmode(orangepi.3b.BOARD) or GPIO.setmode(orangepi.3b.BCM)
"""

# Orange Pi 3B physical board pin to GPIO pin
BOARD = {
    3: 140,    # SDA.2
    5: 141,    # SCL.2
    7: 147,    # PWM15
    8: 25,     # RXD.2
    10: 24,    # TXD.2
    11: 118,   # GPIO3_C6
    12: 119,   # GPIO3_C7
    13: 128,   # GPIO4_A0
    15: 130,   # TXD.7
    16: 131,   # RXD.7
    18: 129,   # GPIO4_A1
    19: 138,   # SPI3_TXD
    21: 132,   # TXD.9
    22: 136,   # SPI3_RXD
    23: 139,   # SPI3_CLK
    24: 134,   # SPI3_CS1
    26: 135,   # GPIO4_A7
    27: 32,    # SDA.3
    28: 33,    # SCL.3
    31: 144,   # GPIO3_D4
    32: 145,   # PWM11
    35: 125,   # GPIO3_D5
    36: 120,   # GPIO3_D0
    37: 123,   # GPIO3_D3
    38: 122,   # GPIO3_D2
    40: 121,   # GPIO3_D1
}

# No reason for BCM mapping, keeping it for compatibility
BCM = BOARD
