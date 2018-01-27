"""
This file contains engine timing constants and enumerations.
"""
from enum import Enum


class StarterSignals(Enum):
    """
    This class represents possible starter switch states.
    """
    STOP = 0
    START = 1


class EngineStatus(Enum):
    """
    This class represents the status of the engine.
    """
    NOT_RUNNING = 0
    RUNNING = 1


class CrankshaftPositions(Enum):
    """
    This class represents possible crankshaft positions.
    """
    TDC = 0
    RightOfCentre = 1
    BDC = 2
    LeftOfCentre = 3
