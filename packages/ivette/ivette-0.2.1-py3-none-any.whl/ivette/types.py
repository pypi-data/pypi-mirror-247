from dataclasses import dataclass
import threading

@dataclass
class ThermoData:
    def __init__(self, energy=None, enthalpy=None, entropy=None, gibbs=None, potential=None):
        self.energy = energy
        self.enthalpy = enthalpy
        self.entropy = entropy
        self.gibbs = gibbs
        self.potential = potential


@dataclass
class Step:
    step: int
    energy: float
    delta_e: float
    gmax: float
    grms: float
    xrms: float
    xmax: float
    walltime: float


@dataclass
class SystemInfo:
    system_id: str
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str
    ntotal: int | None


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
