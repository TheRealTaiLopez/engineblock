"""
This file contains classes and functions to model a camshaft.
"""
import time

from multiprocessing import Pipe, Lock

from engineblock.timing_constants import CrankshaftPositions, EngineStatus, StarterSignals


class Crankshaft():
    """
    This class models an engine's camshaft.
    """

    def __init__(self, solenoid: Pipe, timing_belt: Lock):
        """
        Defines a Crankshaft object to represent an engine's crankshaft.

        :param solenoid: A multiprocessing Pipe that will be used to check for messages from a starter (or similar).
        :param timing_belt: A Lock object that will be used to handle synchronization between processes.
        """
        self.position = CrankshaftPositions.TDC
        self.is_running = EngineStatus.NOT_RUNNING
        self.solenoid = solenoid
        self.timing_belt = timing_belt

    def rotate(self):
        """
        This function rotates the position of the Crankshaft (clockwise) based off its current position.
        """
        if self.position == CrankshaftPositions.TDC:
            self.position = CrankshaftPositions.RightOfCentre
            return
        if self.position == CrankshaftPositions.RightOfCentre:
            self.position = CrankshaftPositions.BDC
            return
        if self.position == CrankshaftPositions.BDC:
            self.position = CrankshaftPositions.LeftOfCentre
            return
        if self.position == CrankshaftPositions.LeftOfCentre:
            self.position = CrankshaftPositions.TDC
            return

    def rotate_process(self, revs_per_minute):
        """
        This function can be used to create a Crankshaft process that rotates a Crankshaft at a given RPM. The process
        loops infinitely, polling the solenoid for signals. If a start signal is seen rotation begins, and will continue
        until a stop signal is seen. The current Crankshaft position is printed every quarter rotation.

        :param revs_per_minute: The RPM to rotate the Crankshaft at.
        """
        revs_per_second = 60 / revs_per_minute
        while True:
            any_signals = self.solenoid.poll()
            if self.is_running is EngineStatus.RUNNING and not any_signals:
                time.sleep(revs_per_second / 4)
                self.rotate()
                self.timing_belt.acquire()
                try:
                    print("current position {}".format(self.position))
                finally:
                    self.timing_belt.release()
                continue

            signal = self.solenoid.recv()
            if (signal is StarterSignals.STOP) and (self.is_running is EngineStatus.RUNNING):
                self.is_running = EngineStatus.NOT_RUNNING
                print("Crankshaft stopped")
                return
            elif signal is StarterSignals.START:
                self.is_running = EngineStatus.RUNNING

