# Personal Finance Tracker — staged development guide

These folders contain the files to introduce or update at each real development milestone. Copy the contents of **one stage** into your Git repository, inspect and test the change, and then commit it. Do not commit the stage folders themselves.

Start with a new empty folder named `Personal_Finance_Tracker`, run `git init`, and copy the contents of stage 01 into the repository root. For each later stage, copy its contents into the same root, preserving paths.

## Commit sequence

### 01 Project Setup

Files: `.gitignore`, `requirements.txt`, `data/.gitkeep` and an initial `README.md`

```bash
git status
git add ".gitignore" "requirements.txt" "data/.gitkeep" "README.md"
git commit -m "Initialize Python project structure and dependency configuration"
```

### 02 Transaction Models

Files: `models/__init__.py`, `models/transaction.py`

```bash
git status
git add "models/__init__.py" "models/transaction.py"
git commit -m "Implement validated transactions with income and expense inheritance"
```

### 03 Finance Logic

Files: `services/__init__.py`, `services/finance_tracker.py`

```bash
git status
git add "services/__init__.py" "services/finance_tracker.py"
git commit -m "Add balance calculations category summaries and monthly budgets"
```

### 04 JSON Storage

Files: `storage/__init__.py`, `storage/json_storage.py`

```bash
git status
git add "storage/__init__.py" "storage/json_storage.py"
git commit -m "Persist finance records with safe JSON file writes"
```

### 05 Command Line

Files: `main.py`

```bash
git status
git add "main.py"
git commit -m "Build interactive command line finance management menu"
```

### 06 Transaction Tests

Files: `tests/__init__.py`, `tests/test_transaction.py`

```bash
git status
git add "tests/__init__.py" "tests/test_transaction.py"
git commit -m "Test transaction validation and income expense behavior"
```

### 07 Finance Tests

Files: `tests/test_finance_tracker.py`

```bash
git status
git add "tests/test_finance_tracker.py"
git commit -m "Test balances spending summaries and budget calculations"
```

### 08 Storage Tests

Files: `tests/test_json_storage.py`

```bash
git status
git add "tests/test_json_storage.py"
git commit -m "Test JSON persistence and invalid data recovery"
```

### 09 Documentation

Files: `README.md`, `PRESENTATION_OUTLINE.md`

```bash
git status
git add "README.md" "PRESENTATION_OUTLINE.md"
git commit -m "Document setup architecture testing and presentation plan"
```

## Verify the finished application

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -v
python3 main.py
```

Only commit after reviewing the code and checking that the milestone works. Intermediate stages may not yet support launching the full application. Use `git log --oneline` to inspect the history. Push to your own GitHub repository when ready.

**Important:** Commit timestamps must reflect real work. This package does not generate a fabricated Git history. Your professor also requires a real unlisted YouTube link at the top of the final README and a viewable slide deck. Replace the placeholder and create your presentation before submission.
