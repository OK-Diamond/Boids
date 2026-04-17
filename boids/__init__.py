"""
Boids flocking simulation — COMP3004/4105 coursework.

Package structure:
    simulation.py  — Config dataclass and Flock class (core engine)
    metrics.py     — polarisation, cluster count, NN distance, time-to-flock
    experiments.py — experiment runner (conditions × trials → CSV)
"""
from .simulation import Config, Flock

__all__ = ["Config", "Flock"]
