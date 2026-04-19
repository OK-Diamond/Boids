"""
Core Boids functionality

Design notes
------------
All agent state is stored in (N, 2) NumPy arrays rather than individual
Python objects. This makes the per-timestep computation fully vectorised:
neighbour detection, force calculation, and position updates all operate
over the entire flock at once with no Python-level loops over agents.

For N=200 and the experiment volumes required (10 trials × ~15 conditions ×
1000 steps) this is fast enough to run in minutes rather than hours.

Environment
-----------
2D continuous toroidal space. Agents wrap at the edges, which eliminates
boundary effects that would otherwise distort experiment results.

Agents
------
Reactive boids with three hard-coded steering behaviours (Reynolds 1987):
    Separation — steer away from nearby neighbours to avoid crowding
    Alignment  — steer toward the average heading of nearby neighbours
    Cohesion   — steer toward the average position of nearby neighbours

Each behaviour produces a force vector. The three are combined as a
weighted sum. Speed is fixed; only heading changes each timestep.

References
----------
Reynolds, C. (1987). Flocks, herds and schools: A distributed behavioral
    model. SIGGRAPH Computer Graphics, 21(4), 25–34.
Vicsek, T. et al. (1995). Novel type of phase transition in a system of
    self-driven particles. Physical Review Letters, 75(6), 1226–1229.
"""

from dataclasses import dataclass
import numpy as np

@dataclass
class Config:
    """
    All simulation parameters in one place.

    Passing a Config to Flock makes it easy to vary a single parameter
    across experiment conditions while keeping everything else constant.

    Parameters
    ----------
    n : int
        Number of boids.
    width, height : float
        World dimensions (arbitrary units). Toroidal (boids wrap at edges Pac-man style).
    dt : float
        Timestep length. Velocities are in units/step, so dt=1.0 means
        positions advance by one full velocity vector each step.
    speed : float
        Fixed agent speed (units per timestep). Only heading changes, not speed.
    perception_radius : float
        How far a boid can "see". Neighbours outside this radius are ignored.
    sep_weight : float
        Scaling factor for the separation steering force.
    ali_weight : float
        Scaling factor for the alignment steering force.
    coh_weight : float
        Scaling factor for the cohesion steering force.
    noise : float
        Standard deviation of angular noise (radians) added to each boid's
        heading every timestep. 0.0 = no noise. Used in Experiment 4.
    seed : int or None
        Random seed for reproducibility. None = non-deterministic.
    """
    # World
    n:                 int   = 50
    width:             float = 100.0
    height:            float = 100.0
    dt:                float = 1.0

    # Agent
    speed:             float = 1.0
    perception_radius: float = 15.0

    # Steering weights
    sep_weight:        float = 1.5
    ali_weight:        float = 1.0
    coh_weight:        float = 1.0

    # Noise (Experiment 4)
    noise:             float = 0.0

    # Reproducibility
    seed:              int | None = None


class Flock:
    """
    A group of boids.
    
    Parameters
    ----------
    config : Config
        Configurations for the boid simulation.

    Attributes
    ----------
    positions  : ndarray, shape (N, 2)
        Current (x, y) position of every boid.
    velocities : ndarray, shape (N, 2)
        Current velocity vector of every boid. Always has magnitude == speed.
    t          : int
        Number of timesteps elapsed since initialisation.
    config        : Config
        The Config object this Flock was created with.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self._rng = np.random.default_rng(config.seed)

        self.positions = np.empty((config.n, 2), dtype=float)
        self.velocities = np.empty((config.n, 2), dtype=float)
        for i in range(config.n):
            self.positions[i] = np.array([self._rng.uniform(0.0, config.width), self._rng.uniform(0.0, config.height)])
            angle = self._rng.uniform(0.0, 2.0 * np.pi)
            self.velocities[i] = np.array([np.cos(angle), np.sin(angle)]) * config.speed

        self.t: int = 0

    def _neighbour_data(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate neighbourhood.
        This computed the displacement, distances, and neighbour mask for every pair of boids.

        Returns
        -------
        displacement : ndarray[float] (N, N, 2)
            displacement[i, j] is the vector from boids i to j.
        dists : ndarray[float] (N, N)
            Euclidean distance between every pair of boids (toroidal). The diagonal is set to -1 so a boid never counts itself.
        mask  : ndarray[bool] (N, N)
            mask[i, j] is True when boid j is a neighbour of boid i (i.e. within perception_radius).
        """
        config = self.config


        # Displacement from i to j: displacement[i, j] = pos[j] - pos[i]
        # Broadcasting: (1, N, 2) - (N, 1, 2) → (N, N, 2)
        displacement = (
            self.positions[np.newaxis, :, :]   # shape (1, N, 2)
            - self.positions[:, np.newaxis, :] # shape (N, 1, 2)
        )

        # [:, :, 0] means 'all x displacements', [:, :, 1] means 'all y displacements'.
        # If displacement is > half the map then wrapping around the map edge is shorter, so subtract the map size to get the correct negative displacement.
        # If it's < half the world, leave it as is.
        displacement[:, :, 0] -= config.width  * np.round(displacement[:, :, 0] / config.width)
        displacement[:, :, 1] -= config.height * np.round(displacement[:, :, 1] / config.height)

        # Pythagoras to get the distance for each pair
        dists = np.sqrt((displacement ** 2).sum(axis=2))

        # Exclude self from neighbourhood by setting values to -1 (to indicade invalid)
        np.fill_diagonal(dists, -1.0)

        # Neighbour mask
        mask = np.logical_and(dists < config.perception_radius, dists > 0)  # (N, N) bool

        return displacement, dists, mask

    def _separation_force(self, displacements: np.ndarray, dists: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Separation: steer away from nearby neighbours to avoid crowding.

        Each neighbour contributes a repulsion vector pointing directly away from it.
        The direction is weighted so closer neighbours contribute more.

        Parameters
        ----------
        displacements, dists, mask : outputs from _neighbour_data()

        Returns
        -------
        force : ndarray[float] (N, 2)
        """

        # calc direction weighting - closer neighbours affect direction more
        weights = np.where(mask, 1.0 / dists ** 1, 0.0) # (N, N)

        # Weighted sum of repulsion vectors
        seperation_vects = -(displacements * weights[:, :, np.newaxis]).sum(axis=1) # (N, 2)

        # Normalise to unit vector & zero out if no neighbours
        magnitude = np.linalg.vector_norm(seperation_vects, axis=1, keepdims=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            force = np.where(magnitude > 1e-8, seperation_vects / magnitude, 0.0)

        return force

    def _alignment_force(self, mask: np.ndarray) -> np.ndarray:
        """
        Alignment: steer toward the average heading of nearby neighbours.

        Sums the velocity vectors of all neighbours, then normalises it.

        Parameters
        ----------
        mask : output from _neighbour_data()

        Returns
        -------
        force : ndarray[float] (N, 2)
        """
        # Sum neighbour velocities
        neighbour_velocities = (
            self.velocities[np.newaxis, :, :] # (1, N, 2)
            * mask[:, :, np.newaxis]          # (N, N, 1)
        ).sum(axis=1)                         # (N, 2)

        # Normalise & zero out if no neighbours
        magnitude = np.linalg.vector_norm(neighbour_velocities, axis=1, keepdims=True)  # (N, 1)
        with np.errstate(divide='ignore', invalid='ignore'):
            force = np.where(magnitude > 1e-8, neighbour_velocities / magnitude, 0.0)
        return force

    def _cohesion_force(self, displacements: np.ndarray, mask:  np.ndarray) -> np.ndarray:
        """
        Cohesion: steer toward the average position of nearby neighbours.

        Uses the toroidal displacement vectors rather than raw positions, so cohesion works correctly across the wrapped boundary.

        Parameters
        ----------
        displacements, mask : outputs from _neighbour_data()

        Returns
        -------
        force : ndarray[float] (N, 2)
        """
        neighbour_count = mask.sum(axis=1, keepdims=True).astype(float)  # (N, 1)

        # Average displacement to neighbours
        avg_disp = (displacements * mask[:, :, np.newaxis]).sum(axis=1)        # (N, 2)
        with np.errstate(divide='ignore', invalid='ignore'):
            avg_disp = np.where(neighbour_count > 0, avg_disp / neighbour_count, 0.0)

        # Normalise & zero out if no neighbours
        magnitude = np.linalg.vector_norm(avg_disp, axis=1, keepdims=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            force = np.where(magnitude > 1e-8, avg_disp / magnitude, 0.0)
        return force


    def step(self) -> None:
        """
        Advance the simulation by one step.
        """
        config = self.config
        # 1. Compute neighbour relationships (toroidal distances + mask).
        displacements, dists, mask = self._neighbour_data()

        # 2. Compute separation, alignment, and cohesion force vectors.
        sep = self._separation_force(displacements, dists, mask)
        ali = self._alignment_force(mask)
        coh = self._cohesion_force(displacements, mask)

        # 3. Combine forces as a weighted sum.
        steering = (
            config.sep_weight * sep
            + config.ali_weight * ali
            + config.coh_weight * coh
        )

        # 4. Add steering to current velocity, then renormalise to fixed speed.
        # Boids with a near-zero resultant (edge case) keep their old heading.
        new_vel = self.velocities + steering
        magnitude = np.linalg.vector_norm(new_vel, axis=1, keepdims=True)
        self.velocities = np.where(
            magnitude > 1e-8,
            new_vel / magnitude * config.speed,
            self.velocities,
        )

        # 5. Add angular noise
        # Angular noise: rotate each heading by a Gaussian-sampled angle.
        # This is used in Experiment 4 to test robustness to perception error.
        if config.noise > 0.0:
            angles  = np.arctan2(self.velocities[:, 1], self.velocities[:, 0])
            angles += self._rng.normal(0.0, config.noise, size=config.n)
            self.velocities = (
                np.stack([np.cos(angles), np.sin(angles)], axis=1) * config.speed
            )

        # 6. Advance positions & wrap toroidally.
        self.positions = (self.positions + self.velocities * config.dt) % np.array([config.width, config.height])

        self.t += 1

    def run(self, steps: int) -> None:
        """
        Run the simulation for a fixed number of timesteps.

        Use this when you only need the final state. To record metrics at
        every timestep, call step() in a loop instead.

        Parameters
        ----------
        steps : int
            Number of timesteps to advance.
        """
        for _ in range(steps):
            self.step()
