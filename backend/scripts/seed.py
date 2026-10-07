"""CLI script to run database seeding.

Usage:
    python scripts/seed.py
"""

import sys
from pathlib import Path

# Add backend directory to sys.path so app module is importable
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.database.seed import main

if __name__ == "__main__":
    main()
