# Low-Label Output Calibration for Music Emotion Regression

**English** | [简体中文](README.zh-CN.md)

Draft research manuscript and supporting figures for low-label output calibration in cross-dataset music emotion regression.

## Reading Guide

- [English manuscript](manuscript_en.md)
- [HTML version](manuscript_en.html) — GitHub displays the source code; download the repository and open the file locally to read it.
- [Editable Word version](manuscript_en.docx)
- [Figures and captions](figures/captions.md)
- [Literature evidence records](working/literature_evidence.json)

## Research Overview

This study uses frozen MERT music representations and an emotion prediction head trained on DEAM to compare output calibration methods on full-chorus PMEmo recordings, with annotation budgets of 5 or 10 songs.

In the prespecified primary comparison, using 10 annotated songs and an arousal-only offset correction at half strength reduced arousal mean squared error by an average of 13.50% across 334 fixed evaluation risk-group representatives. The manuscript and appendices document dataset roles, complete comparisons, adaptation-pool stability, and the scope of the conclusions.

The manuscript is currently an English-language draft. Author information, formatting for the target journal, and formal submission declarations remain to be added.

## CPU-Based Music Emotion Demo

The application source code is available in [`code/`](code/README.md). It uses a separate React/TypeScript frontend with a Chinese-language interface and a FastAPI backend running on CPU.

The demo supports:

- Audio clip uploads
- Overall valence and arousal predictions
- Window-level prediction curves using 10-second windows and a 5-second hop
- Playback-synchronized visualization
- JSON and CSV exports

The window-level curves are produced by a static model and should not be interpreted as validated second-by-second emotion recognition. Target-domain calibration is disabled by default.

See [`code/README.md`](code/README.md) for startup instructions, downloading the pinned MERT model, and verifying the manuscript's prediction head.

The repository does not include model weights, demo audio, virtual environments, or `node_modules`. The required model assets must be obtained separately after cloning.

The scope of automated testing and actual CPU execution is documented in [`code/VALIDATION.md`](code/VALIDATION.md) and [`code/TIMELINE_UPGRADE-20261012.md`](code/TIMELINE_UPGRADE-20261012.md). Publishing the source code in this repository does not mean that the demo has been deployed as a public website.

## Repository Structure

- `manuscript_en.*`: Manuscript in Markdown, HTML, and Word formats.
- `figures/`: Six figures in PNG, PDF, and SVG formats, captions, and a source-verification manifest.
- `scripts/`: Scripts for figure generation, manuscript structure checks, and document export.
- `working/`: Evidence maps, literature records, section outlines, and revision notes.

## Scripts and Document Generation

Run `python scripts/audit_manuscript.py` from the repository root to check the manuscript structure and file references.

To generate updated HTML and Word versions from the Markdown manuscript, first install the dependencies with `python -m pip install -r scripts/requirements-documents.txt` using Python 3.10 or later. Then run `python scripts/build_manuscript_outputs.py`.

The HTML version uses native MathML to display equations offline in modern Chrome, Edge, or Firefox. The Word version uses Pandoc to convert equations into editable native equation objects. The Markdown version uses GitHub-supported `$...$` and `$$...$$` math delimiters.

Run `python scripts/test_math_rendering.py` to verify the 10 display equations, inline equations, and Word equation structure, and to check that the mathematical expressions remain unchanged relative to the original commit.

Run `python scripts/test_reporting_integrity.py` to check that the complete results tables, appendices, references, and necessary limitations remain consistent before and after revisions to the contribution wording.

GitHub displays HTML files as source code, so open the HTML version locally to read it. For the Markdown manuscript, use GitHub's rendered view rather than the Raw view.

## Data, Models, and Reproducibility

Figure generation requires `numpy`, `matplotlib`, and experimental JSON files from the original workspace's `进度/` directory.

The complete raw experimental outputs, model weights, music audio, and locally installed dependencies are not included in this repository. The repository's `figure_manifest.json` retains source paths and SHA records; these records do not establish that the complete experimental data have been publicly released.

Commercial song audio is not distributed with this repository. See the manuscript and references for data and model sources.
