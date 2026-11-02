"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Verify JSON roundtrips and graceful handling of damaged data.
Resources: Original implementation; Python standard library and pytest documentation.
"""

import json
import pytest
from models.transaction import Income
from services.finance_tracker import FinanceTracker
from storage.json_storage import JsonStorage


def test_missing_file_starts_empty(tmp_path):
    """Start with an empty tracker when no save exists."""
    assert JsonStorage(tmp_path / 'missing.json').load().balance() == 0


def test_save_and_load_roundtrip(tmp_path):
    """Restore transactions and budgets from disk."""
    store = JsonStorage(tmp_path / 'finance.json')
    tracker = FinanceTracker([Income('75.50', 'Work', 'Shift', '2026-10-29')])
    tracker.set_budget('2026-10', 'Food', '100')
    store.save(tracker)
    restored = store.load()
    assert restored.to_dict() == tracker.to_dict()
    assert json.loads(store.path.read_text())['transactions'][0]['type'] == 'Income'


def test_corrupt_json_raises_clear_error(tmp_path):
    """Never silently replace a corrupted existing save."""
    path = tmp_path / 'broken.json'
    path.write_text('{broken', encoding='utf-8')
    with pytest.raises(ValueError, match='Invalid saved data'):
        JsonStorage(path).load()


def test_malformed_data_rejected(tmp_path):
    """Reject structurally invalid but syntactically valid JSON."""
    path = tmp_path / 'broken.json'
    path.write_text('{"transactions": {}, "budgets": {}}', encoding='utf-8')
    with pytest.raises(ValueError):
        JsonStorage(path).load()
