# Tiny Language Lab Requirements Files

## Problem / Motivation

The Tiny Language Lab had no dedicated pip requirements files, making it harder for contributors and users to install the core runtime dependencies separately from optional tooling. Third-party imports across `experiments/tiny_language_lab/*.py` and `docs/release/stage61-flagship/**/*.py` were audited to separate required core packages (`torch`, `numpy`) from optional extras used for figures, Hugging Face release scripts, the Gradio playground, and ONNX export.

## What Changed

| File | Summary |
| --- | --- |
| `experiments/tiny_language_lab/requirements.txt` | Core runtime dependencies (`torch`, `numpy`). |
| `experiments/tiny_language_lab/requirements-extras.txt` | Optional dependencies for figures, Hugging Face release, Gradio playground, and ONNX export. |
| `experiments/tiny_language_lab/README.md` | Added `## Requirements` section referencing both requirements files and a note on installing CUDA `torch` via the PyTorch CUDA wheel index. |
