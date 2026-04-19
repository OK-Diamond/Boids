"""
Trial runner and parameter-sweep.

Provides
--------
    run_trial: one simulation run, returns metrics
    sweep_parameter: many trials across many conditions, writes to CSV
    TrialResult: dataclass holding one trial's metric time-series
"""

import csv
import dataclasses
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .simulation import Config, Flock
from .metrics import polarisation, nearest_neighbour_distance, cluster_count

@dataclass
class TrialResult:
    """
    Time-series of metrics from a single simulation trial.

    All arrays have the same length: one entry per recorded timestep.
    `times` holds the step indices; the other arrays hold the metric values.
    
    Parameters
    ----------
    times : np.ndarray (N)
        Recorded step indices (e.g. [0, 25, 50, ..., 5000])
    polarisation : np.ndarray (N)
        Polarisation values.
    cluster_count : np.ndarray (N)
        Cluster counts.
    nn_distance : np.ndarray (N)
        Mean nearest-neighbour distances.
    """
    times: np.ndarray
    polarisation: np.ndarray
    cluster_count: np.ndarray
    nn_distance: np.ndarray


def run_trial(config: Config, total_steps: int, record_every: int = 25) -> TrialResult:
    """
    Run one simulation trial and record metrics periodically.

    Parameters
    ----------
    config : Config
        Full simulation configuration. `config.seed` controls reproducibility.
    total_steps : int
        Number of timesteps to simulate.
    record_every : int
        Record metrics every N steps. Lower = finer time-series, larger CSV.

    Returns
    -------
    TrialResult
    """
    flock = Flock(config)

    result = TrialResult(
        times=np.array([], dtype=int),
        polarisation=np.array([], dtype=float),
        cluster_count=np.array([], dtype=int),
        nn_distance=np.array([], dtype=float)
    )

    for step in range(total_steps):
        if step % record_every == 0:
            result.times = np.append(result.times, step)
            result.polarisation = np.append(result.polarisation, polarisation(flock))
            result.cluster_count = np.append(result.cluster_count, cluster_count(flock))
            result.nn_distance = np.append(result.nn_distance, nearest_neighbour_distance(flock))
        flock.step()

    if total_steps % record_every == 0:
        result.times = np.append(result.times, total_steps)
        result.polarisation = np.append(result.polarisation, polarisation(flock))
        result.cluster_count = np.append(result.cluster_count, cluster_count(flock))
        result.nn_distance = np.append(result.nn_distance, nearest_neighbour_distance(flock))

    return result

def sweep_parameter(
    base_config: Config, 
    param_name: str,
    param_values: list[float],
    output_csv: str,
    trials: int = 10,
    total_steps: int = 5000,
    record_every: int = 25,
    seed: int = 0,
    verbose: bool = True,
) -> None:
    """
    Sweep one Config field across a set of values, running `trials` repeats per value.
    Writes a single long-format CSV with all results.

    Each trial gets a deterministic seed of (seed_base + condition_index*trials + trial_index), so the whole sweep is reproducible and trials within a single condition use different seeds.

    Parameters
    ----------
    base_config : Config
        Baseline config. All fields used as-is except for `param_name`.
    param_name : str
        Name of the Config field to vary (e.g. "ali_weight", "n", "noise").
    param_values : list of values
        Values to use for `param_name` across conditions.
    output_csv : str
        Path to the CSV file to write (will be overwritten if it exists).
    trials : int
        Trials per condition.
    total_steps : int
    record_every : int
    seed : int
        Offset for the random seeds. Essentially the seed for the whole sweep.
    verbose : bool
        Print progress as the sweep runs.
    """
    # Ensure the output directory exists (e.g. results/)
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_conditions = len(param_values)
    total_trials = n_conditions * trials
    t_start = time.perf_counter()

    if verbose:
        print(f"Test {n_conditions} values of {param_name} for {trials} trials of {total_steps} steps each")

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "param_name", "param_value", "trial", "step",
            "polarisation", "cluster_count", "nn_distance",
        ])

        for cond_i, value in enumerate(param_values):
            for trial in range(trials):
                trial_seed   = seed + cond_i * trials + trial
                config = dataclasses.replace(
                    base_config, **{param_name: value, "seed": trial_seed},
                )
                result = run_trial(config, total_steps, record_every)

                # One CSV row per recorded timestep
                for i, step in enumerate(result.times):
                    writer.writerow([
                        param_name,
                        value,
                        trial,
                        int(step),
                        f"{result.polarisation[i]:.6f}",
                        int(result.cluster_count[i]),
                        f"{result.nn_distance[i]:.6f}",
                    ])

                if verbose:
                    elapsed = time.perf_counter() - t_start
                    print(
                        f"  [{((cond_i * trials) + trial + 1):3d}/{total_trials}] "+
                        f"{param_name}={value:.2f} trial={trial} "+
                        f"final_pol={result.polarisation[-1]:.3f}  "+
                        f"(elapsed {elapsed:.1f}s)"
                    )

    if verbose:
        total_elapsed = time.perf_counter() - t_start
        print(f"Done. Wrote {output_csv} in {total_elapsed:.1f}s.")
