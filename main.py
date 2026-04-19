"""
main.py — Sanity-check runner for the Boids simulation.

Runs a single simulation and checks that flocking actually emerges:
  - Polarisation should start near 0 (random headings) and rise toward 1.
  - Saves a three-panel position snapshot to plots.

This file is NOT part of the experiment pipeline (that lives in
experiments.py, added in Week 3). It is just a quick visual/numerical check
that the simulation behaves as expected before running experiments.
"""

from dataclasses import dataclass

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from boids import Config, Flock, polarisation

matplotlib.use("svg")  # non-interactive backend (no window needed)


@dataclass
class SnapshotData:
    """
    Data structure for a snapshot of the simulation, used for plotting.
    
    Parameters
    ----------
    timestep : int
        The simulation step at which the snapshot was taken.
    positions : np.ndarray
        An (N, 2) array of boid positions at the snapshot time.
    velocities : np.ndarray
        An (N, 2) array of boid velocities at the snapshot time.
    config : Config
        The configuration parameters of the simulation (used for plot titles).
    """
    timestep: int
    positions: np.ndarray
    velocities: np.ndarray
    config: Config

def save_snapshot(snapshots: list[SnapshotData], filename: str = "plots/sanity_check", file_format: str = "svg") -> None:
    """
    Save a row of scatter-plot frames to a file.

    Parameters
    ----------
    snapshots : list of (timestep, positions, velocities, cfg)
    filename  : output path (relative to project root). Do NOT include file extension.
    file_format : output file format (e.g. "svg", "png"). Must match the matplotlib backend in use.
    """
    filename = f"{filename}.{file_format}"
    n_frames = len(snapshots)
    fig, axes = plt.subplots(1, n_frames, figsize=(5 * n_frames, 5))
    if n_frames == 1:
        axes = [axes]

    for axis, snapshot in zip(axes, snapshots):
        axis.scatter(snapshot.positions[:, 0], snapshot.positions[:, 1], s=7, color="blue", alpha=0.6)

        # Draw a heading arrow on each boid
        axis.quiver(
            snapshot.positions[:, 0], snapshot.positions[:, 1],
            snapshot.velocities[:, 0], snapshot.velocities[:, 1],
            scale=1 / (snapshot.config.width * 0.03),
            scale_units="xy",
            width=0.003,
            color="blue",
            alpha=0.6,
        )

        axis.set_xlim(0, snapshot.config.width)
        axis.set_ylim(0, snapshot.config.height)
        axis.set_aspect("equal")
        axis.set_title(f"t = {snapshot.timestep}")
        # axis.set_xlabel("x")
        # axis.set_ylabel("y")

    fig.suptitle(
        f"Boids | "+
        f"N={snapshots[0].config.n} "+
        f"sep={snapshots[0].config.sep_weight} "+
        f"ali={snapshots[0].config.ali_weight} "+
        f"coh={snapshots[0].config.coh_weight}",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"  Snapshot saved: {filename}")

def main() -> None:
    """
    Run a single simulation and save snapshots
    """
    config = Config(
        n                 = 80,
        width             = 3000.0,
        height            = 3000.0,
        speed             = 1.0,
        perception_radius = 150.0,
        sep_weight        = 1.0,
        ali_weight        = 1.0,
        coh_weight        = 1.0,
        noise             = 0.0,
        seed              = 42,
        #seed              = np.random.randint(1, 100),
    )

    flock     = Flock(config)
    snapshots: list[SnapshotData] = []
    snap_at   = {0, 500, 5000}
    total     = 5000

    print(f"Running simulation for {total} steps")
    print(f"{'Step':>6}  {'Polarisation':>12}")
    print("-" * 22)

    for step in range(total + 1):
        if step in snap_at:
            snapshots.append(SnapshotData(
                timestep=step,
                positions=flock.positions.copy(),
                velocities=flock.velocities.copy(),
                config=config
            ))

        pol = polarisation(flock)
        if step % 100 == 0:
            print(f"{step:>6}  {pol:>12.4f}")

        if step < total:
            flock.step()

    print("-" * 22)
    print()

    pol_start = polarisation(Flock(config))          # fresh flock (same seed)
    pol_end   = polarisation(flock)
    print(f"Polarisation at t=0   : {pol_start:.4f}")
    print(f"Polarisation at t={total} : {pol_end:.4f}")
    print()

    if pol_end > 0.5 or pol_end > pol_start * 1.5:
        print("PASS | Flocking is >0.5 or has increased by 50%.")
    else:
        print("FAIL | Polarisation is low and didn't increase significantly.")

    save_snapshot(snapshots)


if __name__ == "__main__":
    main()
