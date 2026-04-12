# Boids Flocking Simulation
**Designing Intelligent Agents — Project Brief & Progress Plan**

Submission: **14 May 2026** | Topic Approval: **13 March 2026**

---

## 1. Project Brief

### Overview

This project implements a headless Boids flocking simulation and uses it to run structured experiments investigating how the core algorithm parameters and environmental conditions affect emergent flocking behaviour. The focus is on rigorous measurement and analysis — no interactive visualisation is required.

### Environment

A 2D continuous toroidal space (agents wrap at edges, eliminating boundary effects). Agents are initialised at random positions with random headings. The environment is implemented from scratch in Python using NumPy for vectorised computation — no external simulation framework required.

### Agents

Each agent is a Boid implementing the three classic steering behaviours:

- **Separation** — steer away from nearby neighbours to avoid crowding
- **Alignment** — steer toward the average heading of nearby neighbours
- **Cohesion** — steer toward the average position of nearby neighbours

Each behaviour produces a force vector; the three are combined as a weighted sum. Agent speed is fixed; only heading changes. A perception radius determines which neighbours are visible to each agent.

### Research Question

How do the three weighting parameters (separation, alignment, cohesion), flock size, and perceptual noise affect the degree and stability of emergent flocking behaviour?

### Metrics

- **Polarisation (order parameter)** — magnitude of mean unit velocity vector. 0 = chaos, 1 = perfect alignment. **Primary metric.**
- Number of distinct clusters — distance-based grouping count per timestep
- Average nearest-neighbour distance — measure of cohesion/spread
- Time-to-flock — timesteps until polarisation first exceeds 0.8

### Planned Experiments

Each experiment runs the simulation 10 times per condition and reports mean ± std. Plots show metric vs. parameter value.

- **Exp 1** — Sweep alignment weight (0.0–2.0), holding separation and cohesion fixed. Measure polarisation at steady state.
- **Exp 2** — Sweep separation weight (0.0–2.0). Measure cluster count and nearest-neighbour distance.
- **Exp 3** — Vary flock size (N = 10, 25, 50, 100, 200). Does flocking scale?
- **Exp 4** — Add angular noise to agent perception. How robust is flocking as noise increases?
- **Exp 5 (stretch)** — Compare a hard-coded reactive agent against a learned policy (Q-learning on heading choice).

### Topic Approval Text *(submit by 13 March)*

> I plan to implement a headless Boids flocking simulation in Python and use it to investigate how the three core steering parameters (separation, alignment, cohesion weights), flock size, and perceptual noise affect the emergence and stability of collective flocking behaviour. The environment is a 2D toroidal continuous space; agents are simple reactive boids with no learning. The primary metric is polarisation (the magnitude of the mean unit velocity vector, standard in swarm intelligence literature), supplemented by cluster count and nearest-neighbour distance. Experiments will systematically sweep each parameter across a range, running 10 trials per condition and reporting mean ± std. If time permits, a stretch goal is to compare the reactive boid against a simple Q-learning agent that selects heading adjustments. The project requires no external simulation framework and no interactive visualisation, keeping scope well-controlled.

---

## 2. Progress Schedule

Target: **9 hours/week over 10 weeks = 90 hours total.** Weeks are conservative — the earlier weeks are lighter to account for other coursework load. **Do not skip the checkpoints.**

> ⚠️ If you miss a checkpoint by more than 3 days, you must drop Experiment 5 (stretch goal) immediately to protect core scope.

---

### Week 1 — 4–10 Mar · 8 hrs

- Set up repo and Python environment (venv, numpy, matplotlib)
- Read 2 papers: Reynolds 1987 (original Boids) + Vicsek 1995 (polarisation metric)
- Sketch simulation architecture on paper before writing any code
- Write topic approval text and submit to Moodle

### 🎯 DEADLINE: Topic approval submitted — 13 March, 3 pm

---

### Week 2 — 11–17 Mar · 9 hrs

- Implement core agent class: position, velocity, heading update
- Implement separation, alignment, cohesion force vectors
- Basic simulation loop running (no metrics yet)
- Sanity-check: agents should start visibly clustering

### Week 3 — 18–24 Mar · 10 hrs

- Implement all four metrics: polarisation, cluster count, NN-distance, time-to-flock
- Write experiment runner: loop conditions × trials, collect results to CSV
- Run Experiment 1 (alignment weight sweep) end-to-end
- Verify output looks sensible — polarisation should rise with alignment weight

### Week 4 — 25–31 Mar · 8 hrs

- Run Experiment 2 (separation weight sweep)
- Run Experiment 3 (flock size scaling)
- Generate and save all plots (matplotlib, label axes properly)
- Easter break buffer — minimum: experiments 1–3 must be complete

### 🎯 DEADLINE: Checkpoint — Experiments 1–3 complete, plots generated — 31 March

---

### Week 5 — 1–7 Apr · 9 hrs

- Run Experiment 4 (perceptual noise)
- Collate all results, check for anomalies or runs to repeat
- Begin report outline: paste in question, method, experiment design sections

### Week 6 — 8–14 Apr · 9 hrs

- Write Introduction and Background sections of report (with paper citations)
- Write Methodology section (environment, agents, metrics, experiment design)
- Decide whether Experiment 5 is feasible — if not, cut it now

### 🎯 DEADLINE: Checkpoint — Report introduction + methodology drafted — 14 April

---

### Week 7 — 15–21 Apr · 10 hrs

- Write Results section — describe each experiment's findings, reference plots
- Write Discussion — answer the research question using experimental evidence
- Identify limitations honestly (they're worth marks)

### Week 8 — 22–28 Apr · 9 hrs

- Write Conclusion section
- Full read-through: check word count (2500–4000), fix structure and flow
- Check code is commented; push to repo or zip for supplementary material

### 🎯 DEADLINE: Checkpoint — Full report draft complete — 28 April

---

### Week 9 — 29 Apr–5 May · 8 hrs

- Polish report: fix any weak sections, improve chart labels and captions
- Add any missing references (aim for 6+ papers cited)
- Buffer for anything that slipped — do not start new experiments

### Week 10 — 6–13 May · 6 hrs

- Final proof-read
- Confirm submission package: report + code + any supplementary material
- Submit via Moodle before 3pm on 14 May

### 🎯 DEADLINE: FINAL SUBMISSION — 14 May 2026, 3 pm

---

## 3. Scope Management

| | Core (must do) | Should do | Stretch |
|---|---|---|---|
| | Boids simulation: separation, alignment, cohesion | Experiment 4 — noise robustness | Experiment 5 — Q-learning vs reactive boid |
| | Polarisation metric + at least one secondary metric | 6+ cited papers | |
| | Experiments 1–3 (parameter sweeps + flock size scaling) | | |
| | Report with research question, methodology, results, discussion | | |

> ⚠️ Do not add interactive visualisation. It eats time and earns zero extra marks.

> ⚠️ Do not gold-plate the simulation. More experiments with good analysis beats fewer with perfect code.

---

## Papers to Read (in order)

1. Reynolds, C. (1987). *Flocks, herds and schools: A distributed behavioral model.* SIGGRAPH. — the original, cite in background
2. Vicsek, T. et al. (1995). *Novel type of phase transition in a system of self-driven particles.* Physical Review Letters. — source of the polarisation metric
3. Couzin, I. et al. (2002). *Collective memory and spatial sorting in animal groups.* Journal of Theoretical Biology. — good context for parameter regimes
4. Any 1–2 review papers on swarm intelligence / multi-agent systems for broader background
