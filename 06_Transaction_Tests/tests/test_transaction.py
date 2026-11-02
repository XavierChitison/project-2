"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Verify transaction validation, inheritance, and serialization.
Resources: Original implementation; Python standard library and pytest documentation.
"""

from decimal import Decimal
import pytest
from models.transaction import Expense, Income, Transaction


def test_income_and_expense_have_opposite_signs():
    """Verify inheritance-based signed amount calculations."""
    income = Income('120.50', 'Salary', 'Pay', '2026-10-29')
    expense = Expense('20.25', 'Food', 'Lunch', '2026-10-29')
    assert isinstance(income, Transaction)
    assert income.signed_amount() == Decimal('120.50')
    assert expense.signed_amount() == Decimal('-20.25')


@pytest.mark.parametrize('amount', ['0', '-1', 'NaN', 'Infinity', '1.001', 'abc'])
def test_invalid_amount_rejected(amount):
    """Reject invalid and imprecise money values."""
    with pytest.raises(ValueError):
        Expense(amount, 'Food', '', '2026-10-29')


def test_transaction_json_roundtrip():
    """Preserve subclass and values through dictionary conversion."""
    original = Expense('9.99', 'Food', 'Snack', '2026-10-29')
    assert Transaction.from_dict(original.to_dict()) == original


def test_invalid_date_rejected():
    """Reject impossible calendar dates."""
    with pytest.raises(ValueError):
        Income('5', 'Gift', '', '2026-02-30')


def test_unknown_transaction_type_rejected():
    """Reject unknown transaction types in stored data."""
    with pytest.raises(ValueError):
        Transaction.from_dict({'type': 'Transfer'})
