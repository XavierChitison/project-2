"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Verify balances, monthly spending, and budget rules.
Resources: Original implementation; Python standard library and pytest documentation.
"""

from decimal import Decimal
import pytest
from models.transaction import Expense, Income
from services.finance_tracker import FinanceTracker


def test_balance_and_monthly_spending():
    """Calculate signed balances and filter expenses by month."""
    tracker = FinanceTracker()
    tracker.add_transaction(Income('1000', 'Job', '', '2026-10-01'))
    tracker.add_transaction(Expense('125.25', 'Food', '', '2026-10-02'))
    tracker.add_transaction(Expense('30', 'Food', '', '2026-09-29'))
    assert tracker.balance() == Decimal('844.75')
    assert tracker.spending_by_category('2026-10') == {'Food': Decimal('125.25')}


def test_budget_can_show_overspending():
    """Show negative remaining funds when expenses exceed a budget."""
    tracker = FinanceTracker([Expense('60', 'Food', '', '2026-10-15')])
    tracker.set_budget('2026-10', 'Food', '50')
    assert tracker.budget_status('2026-10', 'Food')['remaining'] == Decimal('-10.00')


@pytest.mark.parametrize('amount', ['-1', 'NaN', '1.001'])
def test_invalid_budget_rejected(amount):
    """Reject invalid budget amounts."""
    with pytest.raises(ValueError):
        FinanceTracker().set_budget('2026-10', 'Food', amount)


def test_invalid_month_rejected():
    """Reject invalid month identifiers."""
    with pytest.raises(ValueError):
        FinanceTracker().spending_by_category('2026-13')
