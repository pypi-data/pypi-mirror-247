from dataclasses import dataclass
import threading

@dataclass
class ThermoData:
    def __init__(self, energy=None, enthalpy=None, entropy=None, gibbs=None, potential=None):
        self.energy = energy  # Total energy
        self.temp: float | None = None  # Temperature
        self.freq_scale: float | None = None  # Frequency scaling parameter
        self.zpe: float | None = None  # Zero-point correction to energy
        self.te: float | None = None  # Thermal correction to energy
        self.th: float | None = None  # Thermal correction to enthalpy
        self.ts: float | None = None  # Total entropy
        self.ts_trans: float | None = None  # Translational entropy
        self.ts_rot: float | None = None  # Rotational entropy
        self.ts_vib: float | None = None  # Vibrational entropy
        self.cv: float | None = None  # Cv (constant volume heat capacity)
        self.cv_trans: float | None = None  # Translational Cv
        self.cv_rot: float | None = None  # Rotational Cv
        self.cv_vib: float | None = None  # Vibrational Cv


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
