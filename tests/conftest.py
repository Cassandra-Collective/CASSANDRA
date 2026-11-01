"""Keep the lab's sibling imports available without moving research scripts."""

import sys
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1] / "experiments" / "tiny_language_lab"
sys.path.insert(0, str(LAB_DIR))
