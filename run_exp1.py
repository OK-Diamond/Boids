"""
run_exp1.py — Experiment 1: alignment-weight sweep.

Research question addressed
---------------------------
How does the alignment weight affect the degree of emergent flocking
(polarisation) at steady state?

Setup
-----
- Sweep ali_weight from 0.0 to 2.0 in steps of 0.2  (11 conditions)
- 10 trials per condition, independent random seeds  (110 trials total)
- 5000 timesteps per trial
- Separation and cohesion weights held fixed at 1.0
- All other parameters inherited from the base Config below

Output
------
results/exp1_alignment.csv   (long format — see boids/experiments.py docstring)
Console summary table showing mean steady-state polarisation per ali_weight.

Expected result
---------------
Polarisation should rise monotonically with alignment weight, from ≈ 0.1
(random headings, no alignment) to ≈ 0.9+ (strong alignment, tight flock).
"""

import csv
import numpy as np
from boids import Config, sweep_parameter


OUTPUT_CSV    = "results/exp1_alignment.csv"

BASE_CONFIG = Config(
    n = 80,
    width = 3000.0,
    height = 3000.0,
    dt = 1.0,
    speed = 1.0,
    perception_radius = 150.0,
    sep_weight = 1.0,
    ali_weight = 1.0, # overridden by the sweep
    coh_weight = 1.0,
    noise = 0.0,
    seed = None, # overridden by the sweep
)
"""Base config. All fields except ali_weight are fixed across all trials."""

ALI_VALUES = [float(round(x, 2)) for x in np.arange(0.0, 2.01, 0.2)]   # 0.0, 0.2, ..., 2.0
TRIALS = 10
TOTAL_STEPS = 5000
RECORD_EVERY = 25
SEED = 1000

def main() -> None:
    """Run the experiment and print a summary of results."""
    print("=" * 60)
    print("Experiment 1: alignment weight sweep")
    print("=" * 60)
    print(f"ali_weight values : {ALI_VALUES}")
    print(f"trials/condition : {TRIALS}")
    print(f"steps/trial : {TOTAL_STEPS}")
    print(f"record every : {RECORD_EVERY} steps")
    print(f"output : {OUTPUT_CSV}")
    print()

    sweep_parameter(
        base_config = BASE_CONFIG,
        param_name = "ali_weight",
        param_values = ALI_VALUES,
        output_csv = OUTPUT_CSV,
        trials = TRIALS,
        total_steps = TOTAL_STEPS,
        record_every = RECORD_EVERY,
        seed = SEED,
        verbose = True,
    )

    print()
    print_summary(OUTPUT_CSV)


def print_summary(csv_path: str) -> None:
    """
    Print mean & std deviation of the steady-state polarisation per ali_weight value.
    The steady state is approximated as the last 20 of each trial's recorded timesteps.
    """
    # Group polarisation values by (param_value, trial) and collect the step for each, so we can pick the tail of each trial.
    per_trial_series: dict[tuple[float, int], list[tuple[int, float]]] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (float(row["param_value"]), int(row["trial"]))
            if key not in per_trial_series:
                per_trial_series[key] = []
            per_trial_series[key].append((
                int(row["step"]),
                float(row["polarisation"]),
            ))

    # For each trial, take the mean polarisation over the final 20% of samples.
    # Then aggregate those per-trial steady values by param_value.
    per_param_steady: dict[float, list[float]] = {}
    for (param_value, _trial), series in per_trial_series.items():
        series.sort()  # sort by step
        tail_window = max(1, len(series) // 5)
        tail = series[-tail_window:]
        avg_polarisation = float(np.mean([p for _s, p in tail]))
        if param_value not in per_param_steady:
            per_param_steady[param_value] = []
        per_param_steady[param_value].append(avg_polarisation)

    print("Mean steady-state polarisation:")
    print(f"{'ali_weight':>12}  {'mean':>8}  {'std':>8}  {'n':>4}")
    print("-" * 40)
    sorted_values = sorted(per_param_steady.keys())
    for value in sorted_values:
        vals = np.array(per_param_steady[value])
        print(f"{value:>12.2f}  {vals.mean():>8.3f}  {vals.std():>8.3f}  {len(vals):>4d}")

    # Sanity verdict: low vs high end of the sweep
    low  = float(np.mean(per_param_steady[sorted_values[0]]))
    high = float(np.mean(per_param_steady[sorted_values[-1]]))
    print()
    if high > low + 0.3:
        print(f"PASS | Polarisation rises with ali_weight ({low:.2f} -> {high:.2f})")
    else:
        print(f"FAIL | ali_weight does not have a significant positive effect on polarisation ({low:.2f} -> {high:.2f})")


if __name__ == "__main__":
    main()
