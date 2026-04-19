"""
Quantitative measures of flocking behaviour.

All metrics operate on a Flock object except for time_to_flock, which operates on a polarisation time-series.

Provides
-------
toroidal_distances: full pairwise distance matrix under minimum-image convention (world wraparound)
polarisation: Vicsek order parameter.
nearest_neighbour_distance: mean distance to each boid's closest neighbour.
cluster: assign a cluster ID to each boid, where boids in the same cluster are all connected by links of distance < threshold.
cluster_count: number of distinct clusters in the flock.
time_to_flock: first index in the polarisation series at which polarisation >= threshold.


References
----------
Vicsek, T. et al. (1995). Novel type of phase transition in a system of
    self-driven particles. Physical Review Letters, 75(6), 1226–1229.
"""

from __future__ import annotations

import numpy as np

from .simulation import Flock


def toroidal_distances(
    positions: np.ndarray,
    width: float,
    height: float,
) -> np.ndarray:
    """
    Compute the full pairwise distance matrix. This accounts for world wraparound.
    (terms: minimum-image convention, toroidal world)

    This mirrors the logic inside Flock._neighbour_data() but is exposed as
    a standalone helper so metrics can work at arbitrary thresholds without
    needing to go through the simulation's perception-radius mask.

    Parameters
    ----------
    positions : ndarray (N, 2)
    width, height : world dimensions

    Returns
    -------
    dists : ndarray (N, N)
    """
    # Pairwise displacement tensor: displacement[i, j] = positions[j] - positions[i]
    displacement = (
        positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    )

    # Minimum-image wrap on each axis
    displacement[:, :, 0] -= width  * np.round(displacement[:, :, 0] / width)
    displacement[:, :, 1] -= height * np.round(displacement[:, :, 1] / height)

    # Euclidean distances
    dists = np.sqrt((displacement ** 2).sum(axis=2))
    np.fill_diagonal(dists, np.inf)
    return dists


def polarisation(flock: Flock) -> float:
    """
    Magnitude of the mean unit velocity vector.
    Ranges from 0 (completely disordered headings) to 1 (perfect alignment).

    Parameters
    ----------
    flock : Flock

    Returns
    -------
    float in [0, 1]
    """
    # Divide each velocity by its own magnitude to get unit vectors
    unit_vels = flock.velocities / np.linalg.vector_norm(flock.velocities, axis=1, keepdims=True)
    # Find the mean value, i.e. the average movement vector
    mean_vel = unit_vels.mean(axis=0)
    # Find the magnitude. If all boids point in the same direction, this will be 1; if they point in exactly opposite directions, this will be 0
    return float(np.linalg.vector_norm(mean_vel))


def nearest_neighbour_distance(flock: Flock) -> float:
    """
    Mean of each boid's minimum distance to any other boid.
    Low values indicate a tight flock; high values indicate a dispersed one.

    Parameters
    ----------
    flock : Flock

    Returns
    -------
    float (in world units)
    """
    dists = toroidal_distances(flock.positions, flock.config.width, flock.config.height)
    # .min(axis=1) returns each boid's nearest-neighbour distance
    return float(dists.min(axis=1).mean())


def cluster(flock: Flock, threshold: float) -> np.ndarray:
    """
    Assign a cluster value to each boid, where boids in the same cluster are all connected by links of distance < threshold.

    Parameters
    ----------
    flock : Flock
    threshold : float

    Returns
    -------
    clusters : np.ndarray (N)
        1D array of cluster values, where boids in the same cluster have the same value.
    """
    if threshold is None:
        threshold = flock.config.perception_radius

    dists = toroidal_distances(flock.positions, flock.config.width, flock.config.height)

    # eye(n) creates an identity matrix so boids count themselves as adjacent, which simplifies the label propagation logic later.
    boid_count = dists.shape[0]
    adjacent = (dists < threshold) | np.eye(boid_count, dtype=bool)

    # Create an array where each boid stores a value, initally its own index
    labels = np.arange(boid_count)

    while True:
        # Filter so each boid only "sees" the values of its adjacent boids
        masked = np.where(adjacent, labels[np.newaxis, :], np.inf) # non-neighbours = inf (>= any real label)
        # Each boid stored the minimum value it can see (including its own)
        new_labels = masked.min(axis=1)
        # If no values changed, we've converged and can stop
        if np.array_equal(new_labels, labels):
            # All boids in a cluster now have the same stored value.
            return new_labels
        labels = new_labels


def cluster_count(flock: Flock, threshold: float | None = None) -> int:
    """
    Number of distinct groupings/clusters in the flock.

    A cluster is a connected component of the graph where all boids are chained together in a link where they are within `threshold` of each other.

    Parameters
    ----------
    flock : Flock
    threshold : float
        Maximum distance for two boids to count as connected. Defaults to flock.config.perception_radius.

    Returns
    -------
    clusters : int
        Number of distinct clusters.
    """
    if threshold is None:
        threshold = flock.config.perception_radius

    clusters = cluster(flock, threshold)

    return int(np.unique(clusters).size)


def time_to_flock(polarisation_series: np.ndarray, threshold: float = 0.8) -> int | None:
    """
    First index in the polarisation series at which polarisation >= threshold.

    Returns None if the threshold is never reached.

    Typically applied to a whole run's polarisation time-series (produced by
    the experiment runner) rather than called per-step.

    Parameters
    ----------
    polarisation_series : 1D array-like of floats
    threshold : float, default 0.8

    Returns
    -------
    int index, or None if threshold never crossed.
    """
    arr     = np.asarray(polarisation_series)
    reached = np.flatnonzero(arr >= threshold)
    if reached.size == 0:
        return None
    return int(reached[0])
