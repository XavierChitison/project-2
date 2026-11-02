"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Run the interactive command-line personal finance tracker.
Resources: Original implementation; Python standard library and pytest documentation.
"""

from datetime import date
from decimal import Decimal
from models.transaction import Expense, Income
from storage.json_storage import JsonStorage


def prompt_transaction(kind):
    """Collect and validate a new transaction from the user."""
    amount = input('Amount: $').strip()
    category = input('Category: ').strip()
    description = input('Description: ').strip()
    entered_date = input('Date YYYY-MM-DD (Enter for today): ').strip() or date.today().isoformat()
    return kind(amount, category, description, entered_date)


def display_summary(tracker):
    """Print current balance and category spending totals."""
    print(f'\nCurrent balance: ${tracker.balance():,.2f}')
    print('All-time spending by category:')
    for category, amount in sorted(tracker.spending_by_category().items()):
        print(f'  {category}: ${amount:,.2f}')


def run(storage=None):
    """Run the menu until the user exits, saving after each change."""
    storage = storage or JsonStorage('data/finances.json')
    try:
        tracker = storage.load()
    except (ValueError, OSError) as exc:
        print(f'Unable to load data: {exc}')
        print('Fix or back up the saved file before restarting.')
        return
    while True:
        print('\nPERSONAL FINANCE TRACKER')
        print('1. Add income  2. Add expense  3. View summary')
        print('4. Set monthly budget  5. Check budget  6. Exit')
        try:
            choice = input('Choose 1-6: ').strip()
            if choice in ('1', '2'):
                kind = Income if choice == '1' else Expense
                tracker.add_transaction(prompt_transaction(kind))
                storage.save(tracker)
                print('Transaction saved.')
            elif choice == '3':
                display_summary(tracker)
            elif choice == '4':
                month = input('Month YYYY-MM: ').strip()
                category = input('Category: ').strip()
                amount = input('Budget amount: $').strip()
                tracker.set_budget(month, category, amount)
                storage.save(tracker)
                print('Budget saved.')
            elif choice == '5':
                month = input('Month YYYY-MM: ').strip()
                category = input('Category: ').strip()
                status = tracker.budget_status(month, category)
                print(f"Limit: ${status['limit']:.2f} | Spent: ${status['spent']:.2f} | Remaining: ${status['remaining']:.2f}")
            elif choice == '6':
                print('Goodbye!')
                break
            else:
                print('Please choose a number from 1 to 6.')
        except (ValueError, KeyError, TypeError, OSError) as exc:
            print(f'Operation failed: {exc}')
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye!')
            break


if __name__ == '__main__':
    run()
