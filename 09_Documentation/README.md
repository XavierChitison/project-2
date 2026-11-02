<!-- VIDEO LINK: Replace this line with your actual unlisted YouTube URL after recording. -->
**5-minute project presentation:** [Video link pending — upload your own recording](https://www.youtube.com/)

# Personal Finance Tracker

**Author:** Xavier Chitison  
**Project:** Python Crash Course Chapters 8–11 — Option B (new project)

A Python command-line app to record income and expenses, manage monthly category budgets, and retain financial records between sessions. This is a local educational project; it does not connect to bank accounts.

## Setup

Requires Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Tests

```bash
python -m pytest -v
```

## Architecture

- `models/transaction.py`: validated dataclass, `Income`/`Expense` inheritance, JSON conversion.
- `services/finance_tracker.py`: balance, spending summaries, monthly category budgets.
- `storage/json_storage.py`: JSON persistence with atomic replacement and explicit corrupted-file errors.
- `main.py`: user-facing command-line menu and error messages.
- `tests/`: executable pytest tests of core models, service logic, and storage.

Inheritance is appropriate because income and expense share transaction fields and validation but have different effects on balance. The tracker composes transactions rather than inheriting from them because a tracker *contains* transactions, not *is* a transaction. Money uses `Decimal` to avoid binary floating-point rounding issues. Data is stored in `data/finances.json` and ignored by Git to avoid committing private financial records.

## Features

1. Add income or expenses with amount, category, description, and date.
2. View net balance and category spending.
3. Set a monthly budget per category and check remaining allowance.
4. Automatically save changes and restore data when reopening the program.
5. Display errors for invalid amounts, dates, missing budgets, and damaged saved data.

## Example workflow

Run `python main.py`; choose `1` to add income of `1000`, choose `2` to add a `Food` expense of `25.50`, and choose `3` to view a balance of `$974.50`. Set a `Food` budget for `2026-10` with option `4`, then view its status using option `5`.

## Development record

Commit features incrementally during actual development. Suggested commit sequence: scaffold, models, service calculations, storage, CLI, tests, documentation. Do not claim earlier work dates or fabricate history. If this is a new Option B repository, name it `Personal_Finance_Tracker`.

## Presentation

See [`PRESENTATION_OUTLINE.md`](PRESENTATION_OUTLINE.md) for a five-minute video and slide outline. Replace the placeholder video link at the very top of this README after uploading your unlisted video.
