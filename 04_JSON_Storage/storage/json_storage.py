"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Read and atomically write structured finance data as JSON.
Resources: Original implementation; Python standard library and pytest documentation.
"""

import json
import os
import tempfile
from pathlib import Path
from services.finance_tracker import FinanceTracker


class JsonStorage:
    """Persist finance tracker state in a local JSON file."""

    def __init__(self, path):
        """Store the target data file path."""
        self.path = Path(path)

    def load(self):
        """Load saved state, defaulting only when the file does not exist."""
        try:
            with self.path.open('r', encoding='utf-8') as file:
                return FinanceTracker.from_dict(json.load(file))
        except FileNotFoundError:
            return FinanceTracker()
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
            raise ValueError(f'Invalid saved data in {self.path}: {exc}') from exc

    def save(self, tracker):
        """Write JSON using a temporary file to avoid partial saves."""
        if not isinstance(tracker, FinanceTracker):
            raise TypeError('Expected a FinanceTracker')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=self.path.parent,
                                             prefix='.finance-', suffix='.tmp', delete=False) as file:
                temp_name = file.name
                json.dump(tracker.to_dict(), file, indent=2)
                file.write('\n')
            os.replace(temp_name, self.path)
        finally:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)
