# COMP3004/4105 — Boids Project: Master Reference & Submission Checklist

> **Final submission: 14 May 2026, 3pm via Moodle**
> **Today (reference point): 11 April 2026 — Week 6 of 10**
> **Status: Only Week 1 complete. Weeks 2–5 tasks are all overdue.**

---

## 1. Project Summary

- **Module:** COMP3004 / 4105 — Designing Intelligent Agents (University of Nottingham)
- **Lecturers:** Colin Johnson, Jeremie Clos
- **Topic:** Headless Boids flocking simulation in Python, using structured experiments to investigate how core parameters affect emergent flocking behaviour.
- **Research Question:** How do the three weighting parameters (separation, alignment, cohesion), flock size, and perceptual noise affect the degree and stability of emergent flocking behaviour?
- **Language/Stack:** Python, NumPy, Matplotlib — no external simulation framework, no interactive visualisation.
- **Environment:** 2D continuous toroidal space (agents wrap at edges). Random initial positions and headings.
- **Agent type:** Reactive Boid — hard-coded, no learning. Each agent computes separation + alignment + cohesion force vectors, combines as a weighted sum, updates heading only (fixed speed).

---

## 2. Submission Package (what Moodle needs by 3pm 14 May)

- [ ] **Report** — up to 4000 words (not counting headings/references), written for peers on the degree
- [ ] **Code** — upload or link to git repository
- [ ] **AI Statement** — declare what AI tools were used (required; goes in report or separate doc)
- [ ] **Supplementary material** — sample outputs, plots, CSV results (optional but recommended)
- [ ] *(COMP4105 only)* **10-minute presentation** — likely 15 May 2026 or the following week

> Late penalty: 5% per working day. No extensions without an approved EC/CERF request.

---

## 3. What Has Been Done vs. What Remains

### Done (Week 1)
- [x] Repo and Python environment set up (venv, numpy, matplotlib)
- [x] Read Reynolds 1987 and Vicsek 1995
- [x] Architecture sketch
- [x] Topic approval submitted (13 March deadline)

### Still Required — Code & Experiments

#### Core simulation (Weeks 2–3 — overdue)
- [ ] Agent class: position vector, velocity/heading update
- [ ] Separation force vector
- [ ] Alignment force vector
- [ ] Cohesion force vector
- [ ] Weighted sum combination of the three forces
- [ ] Basic simulation loop (toroidal wrap, fixed speed)
- [ ] Sanity check: agents visibly cluster/flock

#### Metrics (Week 3 — overdue)
- [ ] **Polarisation** (primary): magnitude of mean unit velocity vector (0=chaos, 1=perfect alignment)
- [ ] **Cluster count**: distance-based grouping count per timestep
- [ ] **Average nearest-neighbour distance**: measure of cohesion/spread
- [ ] **Time-to-flock**: timesteps until polarisation first exceeds 0.8

#### Experiment runner (Week 3 — overdue)
- [ ] Loop over conditions × trials, collect results to CSV
- [ ] 10 runs per condition, report mean ± std

#### Experiments

| # | Description | Parameters | Primary metric | Status |
|---|-------------|-----------|----------------|--------|
| 1 | Alignment weight sweep | Alignment: 0.0–2.0; sep/coh fixed | Polarisation at steady state | Not done |
| 2 | Separation weight sweep | Sep: 0.0–2.0 | Cluster count + NN distance | Not done |
| 3 | Flock size scaling | N = 10, 25, 50, 100, 200 | Does flocking scale? | Not done |
| 4 (should) | Perceptual noise | Angular noise sweep | Polarisation robustness | Not done |
| 5 (stretch) | Q-learning vs reactive | — | Comparative | Cut if behind |

> ⚠️ Exp 5 (stretch) should be cut now — per the plan's own rule: if more than 3 days past a checkpoint, drop Exp 5 immediately.

#### Plots (per experiment)
- [ ] Metric vs. parameter value plot for each experiment
- [ ] Properly labelled axes, titles, error bars (mean ± std)
- [ ] Saved as files for inclusion in report

---

## 4. Report Structure

**Word budget: 2500–4000 words (headings and references excluded)**

Target audience: fellow students on the degree — no need to explain basic CS, but do not assume Boids/swarm knowledge.

---

### 4.1 Introduction
- State the research question clearly and early
- Why is flocking/swarm behaviour interesting from an AI/agent perspective?
- Brief overview of what the project does and what it finds
- *Marking hook:* Justify why this is a good model problem for AI/autonomy

### 4.2 Background & Literature Review
Cite at minimum 6 papers (aim for this). Must include:
- Reynolds, C. (1987). *Flocks, herds and schools: A distributed behavioral model.* SIGGRAPH — original Boids
- Vicsek, T. et al. (1995). *Novel type of phase transition in a system of self-driven particles.* Physical Review Letters — source of polarisation metric
- Couzin, I. et al. (2002). *Collective memory and spatial sorting in animal groups.* J. Theoretical Biology — parameter regimes context
- 1–2 swarm intelligence / multi-agent systems review papers (find these)
- *Marking hook:* Explain how each paper is relevant — did you use an idea, contrast your work, or get initial inspiration from it?

### 4.3 Methodology

#### 4.3.1 Environment
- 2D continuous toroidal space
- Dimensions, timestep length, initialisation (random positions, random headings)
- Why toroidal (eliminates boundary effects)

#### 4.3.2 Agent Design
- Reactive Boid architecture (hard-coded, no learning/memory)
- Separation, Alignment, Cohesion — each as a force vector, combined as weighted sum
- Fixed speed; only heading changes
- Perception radius — which neighbours are visible
- Pseudocode or formulae for each force (worth marks for quality of diagrams/pseudocode)

#### 4.3.3 Metrics
- Define all four metrics (polarisation, cluster count, NN distance, time-to-flock)
- Cite Vicsek for polarisation definition
- Justify why polarisation is primary

#### 4.3.4 Experiment Design
- For each experiment: what is varied, what is held fixed, how many trials (10), how results are summarised (mean ± std)
- *Marking hook:* Explain how each experiment is focused on the research question

### 4.4 Implementation
- Technologies: Python, NumPy (vectorised), Matplotlib
- Clarify what code is your own vs. drawn from class examples (required for academic integrity)
- Key implementation challenges (e.g. toroidal distance calculation, vectorisation for performance)
- Note: no interactive visualisation by design (scope decision)

### 4.5 Experiments & Results
One sub-section per experiment. Each should contain:
- Setup description (parameter range, fixed values)
- The plot (figure with caption)
- A short verbal description of what the plot shows

Experiments to cover:
- Exp 1: Alignment weight vs. polarisation — expect polarisation to rise with alignment weight
- Exp 2: Separation weight vs. cluster count + NN distance
- Exp 3: Flock size (N) vs. polarisation — does flocking scale?
- Exp 4: Perceptual noise vs. polarisation — robustness

### 4.6 Discussion
- Return directly to the research question
- Use experimental results as evidence — cite specific findings (e.g. "Experiment 1 showed...")
- Answer honestly — what parameters promote flocking? What breaks it?
- Identify interactions between parameters if found
- *Marking hook:* Nuanced, evidence-based answer is expected — "yes/no" is not enough

### 4.7 Conclusion
- Summarise the work in 1–2 paragraphs
- Reflect on successes and **limitations** (limitations are explicitly worth marks)
- "If I had more time" — brief ideas for next steps (e.g. Exp 5 Q-learning, 3D environment, obstacle avoidance, field of view instead of radius)
- Place work in wider context of AI, agents and autonomous systems

### 4.8 References
- Consistent referencing style throughout (any style, but stick to one)
- Minimum 6 papers cited
- References do NOT count toward the 4000-word limit

---

## 5. Marking Criteria Checklist

From the official marking guide — tick when confident each is addressed:

- [ ] **Intrinsic complexity** — Boids + 4 experiments + metrics is a reasonable scope; Exp 4 (noise) and good analysis lifts complexity
- [ ] **Background research** — ≥6 papers cited, each contextualised in the text (not just listed)
- [ ] **Environment & agent design justified** — explain WHY toroidal, WHY reactive, WHY these metrics
- [ ] **AI/agent ideas from the course used** — reactive agent architecture; swarm intelligence; emergent behaviour from local rules
- [ ] **Clear research question** — stated early, experiments directly address it
- [ ] **Experimental rigour** — 10 trials per condition, mean ± std reported, plots with error bars
- [ ] **Report answers the question using evidence** — Discussion section links findings back to research question
- [ ] **Report clarity & structure** — all 8 sections present, scientific English, labelled charts
- [ ] **Quality of charts/diagrams/pseudocode** — axis labels, units, captions, error bars
- [ ] **Reflection on successes and limitations** — honest, specific, in Conclusion

### Grade band targets
| Band | What it needs |
|------|--------------|
| 70–79 | Core + Exp 4 complete, some stretch/challenge, reflects accurately on limitations, clear professional report |
| 60–69 | Core complete (Exps 1–3), good background, most aims met, structured report |
| 50–59 | Core agents + Exps 1–3 done, basic reflection, decently written |

---

## 6. Remaining Schedule (Compressed — Weeks 6–10)

> You are in Week 6. Weeks 2–5 tasks are all overdue. The priority right now is to build the simulation and run all experiments ASAP so there is time to write.

### This week — Week 6 (8–14 Apr) — Build the whole simulation
- Implement agent class + three force vectors + simulation loop
- Implement all four metrics
- Implement experiment runner (conditions × trials → CSV)
- Run Exp 1 and Exp 2, verify outputs look sensible

### Week 7 (15–21 Apr) — Finish experiments + start report
- Run Exp 3 (flock size) and Exp 4 (perceptual noise)
- Generate and save all plots
- Write Introduction + Background sections

### Week 8 (22–28 Apr) — Core report writing
- Write Methodology section (with pseudocode/formulae)
- Write Implementation section
- Write Results section (one sub-section per experiment)

### Week 9 (29 Apr–5 May) — Discussion, Conclusion, polish
- Write Discussion section
- Write Conclusion section
- Full read-through: word count (aim 3000–3800), structure check, fix weak sections
- Improve chart labels and captions

### Week 10 (6–13 May) — Final checks & submission prep
- Final proof-read
- Add AI statement
- Ensure code is commented (mark what is yours vs. class examples)
- Confirm submission package: report + code + plots/CSVs
- Submit via Moodle before 3pm on 14 May

---

## 7. Key Rules & Gotchas

- **No interactive visualisation** — zero extra marks, big time cost. Headless only.
- **Code comments** — must indicate which functions/classes are your own vs. taken from class examples (academic integrity requirement).
- **AI tools** — must be declared in a statement in the report or portfolio. AI used only for minor grammar correction in the report itself; the work must represent ~90–100 hours of your own effort.
- **Word count** — 2500–4000 words; headings and references excluded. Do not go over 4000.
- **10 trials per condition** — required for valid statistics. Do not skip.
- **Error bars on all plots** — mean ± std. This is explicitly in the marking guidance.
- **Stretch goal (Exp 5)** — formally cut now per the plan's own rule.
- **COMP4105 students only** — 10-minute presentation also required (~15 May), worth 10% of module mark. Portfolio is 90%.
- **Late penalty** — 5% per working day. Hard deadline.

---

## 8. Papers Reading List

| Priority | Paper | Why needed |
|----------|-------|------------|
| Done | Reynolds (1987) SIGGRAPH | Original Boids — cite in Background |
| Done | Vicsek et al. (1995) PRL | Source of polarisation metric — cite when defining it |
| To read | Couzin et al. (2002) J. Theor. Biol. | Parameter regimes context |
| To find | 1–2 swarm intelligence review papers | Broader background, hit 6+ citation target |

---

## 9. Contacts & Resources

- Colin Johnson: Colin.Johnson@nottingham.ac.uk
- Jeremie Clos: Jeremie.Clos@nottingham.ac.uk
- Tuesday classes after Spring break: dedicated coursework support sessions
- Submission: Moodle
