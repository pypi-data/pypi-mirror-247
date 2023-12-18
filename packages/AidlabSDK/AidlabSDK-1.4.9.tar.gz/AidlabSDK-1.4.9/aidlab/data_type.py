"""
Created by Szymon Gesicki on 07.11.2021.
"""

from enum import IntEnum

class DataType(IntEnum):
    """
    Data types that can be received from Aidlab and Aidmed One.
    See the documentation to learn more about each data type.
    """
    ECG = 0
    RESPIRATION = 1
    SKIN_TEMPERATURE = 2
    MOTION = 3
    BATTERY = 4
    ACTIVITY = 5
    ORIENTATION = 6
    STEPS = 7
    HEART_RATE = 8
    SOUND_VOLUME = 10
    RR = 11
    PRESSURE = 12
    RESPIRATION_RATE = 14
    BODY_POSITION = 15

