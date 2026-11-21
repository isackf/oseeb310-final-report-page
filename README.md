# Operating Systems Final Project — Example Repository

**Demonstration topic:** Investigating Operating System Behavior Through System Log Analysis  
**Status:** Teaching example — **not** a completed student project.

[View the report website](docs/index.html) · [Course source datasets](#real-dataset-for-the-final-project) · [Reproduce the example](#run-the-example)

## Research motivation

System logs record events from services and processes. Counts, repeated patterns, and bursts can provide evidence of activity, but an unusual event **does not automatically mean a confirmed failure**.

### Example research questions

1. Which services and event types appear most frequently during the observation period?
2. Are warning/error events evenly distributed over time, or concentrated in specific periods?
3. Do simple anomaly criteria identify time windows that merit manual inspection?

> **Important:** This repository uses **synthetic, illustrative data** generated locally to demonstrate repository organization and reproducible analysis. These results are **not findings from Linux or OpenStack**. For the final project, students must use an independently selected, documented public dataset and produce their own research questions and interpretation.

## Repository structure

```text
.
├── README.md                    # Fast overview and reproduction guide
├── requirements.txt            # Dependencies
├── data/sample/                # Generated illustration only
├── scripts/make_sample.py      # Reproducible synthetic-data generator
├── src/analyze.py              # Reusable analysis and figure generation
├── tests/test_analysis.py      # Basic unit tests
├── docs/index.html             # Complete GitHub Pages report website
├── docs/assets/style.css       # Responsive documentation styling
├── docs/index.md               # Plain Markdown report alternative
├── docs/figures/               # Five generated charts
└── .github/workflows/check.yml # Test workflow
```

## Run the example

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/make_sample.py
python -m src.analyze --input data/sample/illustrative_logs.csv --output docs/figures
python -m unittest discover -s tests -v
```

The analysis creates five charts and `docs/figures/summary.json`. The output is deterministic for the fixed random seed.

## What the figures show

| Figure | Analysis | OS interpretation to investigate |
|---|---|---|
| `01_events_by_service.png` | Event frequency by service | Service activity is not the same as service health |
| `02_events_over_time.png` | Activity timeline | Possible workload changes or recording artifacts |
| `03_severity_distribution.png` | Severity frequencies | A high warning count does not establish system failure |
| `04_errors_over_time.png` | Error-event concentration | Bursts are candidates for investigation |
| `05_hourly_anomaly_flags.png` | Explicit, simple anomaly heuristic | Threshold flags are not verified faults |

## Real dataset for the final project

Use an independently selected subset of **[Loghub Linux](https://github.com/logpai/loghub/tree/master/Linux)** or **[Loghub OpenStack](https://github.com/logpai/loghub/tree/master/OpenStack)**. Document the exact source URL, version, time span, chosen subset, field extraction assumptions, and any labels. **The included CSV loader is for the illustrative sample**, not a universal raw Loghub parser. The parser must be adapted to the chosen dataset's format and verified on real examples.

Never commit credentials, sensitive system records, private user information, or large raw archives. Cite and link to the authoritative dataset rather than redistributing data.

## Final project checklist

- [ ] At least **two testable research questions**
- [ ] At least **three analyses/comparisons**
- [ ] At least **five informative figures or tables**, with units and captions
- [ ] Dataset source, scope, preprocessing and fields documented
- [ ] Findings connected to operating-systems concepts and limitations
- [ ] Reproducible scripts, dependencies, and run instructions
- [ ] Website report, code repository, and group presentation
- [ ] Individual contributions identified

Open `docs/index.html` for a **complete, responsive technical report website** with a sidebar, research questions, dataset profile, methods, five figures with interpretations, discussion, learning outcomes, references and reproducibility. `docs/index.md` remains as a plain Markdown alternative. A repository README should make the project easy to navigate, not duplicate the entire report.

## Publishing on GitHub Pages

GitHub Pages can publish the included static HTML website without any website generator: in **Settings → Pages**, select **Deploy from a branch**, branch `main`, folder `/docs`. After publishing, link your public page from the repository description/README. Verify the actual deployment URL in GitHub Settings; it is not generated by this ZIP file.

## Academic integrity

AI tools may assist with coding and writing, but each team must verify its results, explain its own code, and independently defend its interpretations. Copying this demonstration as a final submission does not satisfy the project requirements.
