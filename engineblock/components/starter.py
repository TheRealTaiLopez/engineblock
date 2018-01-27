"""
This file contains classes and functions to represent an electric starter.
"""
from multiprocessing import Pipe

from engineblock.timing_constants import StarterSignals


class Starter:
    """
    This class represents an electric starter for an engine.
    """

    def __init__(self, solenoid: Pipe):
        """
        Defines a Starter object to represent an electric starter.

        :param solenoid: A Pipe object that will be used to communicate to the component of the engine it will effect.
        """
        self.status = StarterSignals.STOP
        self.solenoid = solenoid

    def start(self):
        """
        If the starter has not been started, send a start signal through the solenoid (Pipe).
        """
        if self.status == StarterSignals.START:
            print("Already started")
        else:
            self.status = StarterSignals.START
            self.solenoid.send(self.status)

    def stop(self):
        """
        If the starter has been started, send a stop signal through the solenoid (Pipe).
        """
        if self.status != StarterSignals.START:
            print("Not started")
        else:
            self.status = StarterSignals.STOP
            self.solenoid.send(self.status)
