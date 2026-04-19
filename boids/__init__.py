"""
Boids simulation package.

Package structure:
    simulation.py: Config dataclass and Flock class (core)
    metrics.py: polarisation, cluster count, NN distance, time-to-flock
    experiments.py: trial runner & parameter-sweep with CSV output
"""
from .simulation  import Config, Flock
from .metrics import polarisation, nearest_neighbour_distance, cluster_count, time_to_flock, toroidal_distances
from .experiments import run_trial, sweep_parameter, TrialResult

__all__ = [
    "Config", "Flock",
    "polarisation", "nearest_neighbour_distance", "cluster_count", "time_to_flock", "toroidal_distances",
    "run_trial", "sweep_parameter", "TrialResult",
]
