"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Calculate balances, spending summaries, and monthly budget usage.
Resources: Original implementation; Python standard library and pytest documentation.
"""

from decimal import Decimal, InvalidOperation
from models.transaction import Expense, Transaction


class FinanceTracker:
    """Manage transactions and monthly category budgets."""

    def __init__(self, transactions=None, budgets=None):
        """Initialize validated transaction and budget collections."""
        self.transactions = []
        self.budgets = {}
        for transaction in transactions or []:
            self.add_transaction(transaction)
        for key, amount in (budgets or {}).items():
            month, category = key.split('|', 1)
            self.set_budget(month, category, amount)

    def add_transaction(self, transaction):
        """Add a validated income or expense object."""
        if not isinstance(transaction, Transaction) or type(transaction) is Transaction:
            raise TypeError('Expected an Income or Expense transaction')
        self.transactions.append(transaction)

    def balance(self):
        """Return the net balance from all transactions."""
        return sum((t.signed_amount() for t in self.transactions), Decimal('0.00'))

    def spending_by_category(self, month=None):
        """Summarize expenses by category, optionally filtering YYYY-MM."""
        if month is not None:
            self._validate_month(month)
        totals = {}
        for transaction in self.transactions:
            if isinstance(transaction, Expense) and (month is None or transaction.transaction_date.startswith(month + '-')):
                totals[transaction.category] = totals.get(transaction.category, Decimal('0.00')) + transaction.amount
        return totals

    @staticmethod
    def _validate_month(month):
        """Reject malformed year-month identifiers."""
        from datetime import date
        if not isinstance(month, str) or len(month) != 7:
            raise ValueError('Month must use YYYY-MM')
        try:
            date.fromisoformat(month + '-01')
        except ValueError as exc:
            raise ValueError('Month must use YYYY-MM') from exc

    def set_budget(self, month, category, amount):
        """Set a nonnegative monthly spending limit for a category."""
        self._validate_month(month)
        if not isinstance(category, str) or not category.strip() or '|' in category:
            raise ValueError('Invalid category')
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError('Budget must be numeric') from exc
        if not value.is_finite() or value < 0 or value.as_tuple().exponent < -2:
            raise ValueError('Budget must be nonnegative with at most two decimal places')
        self.budgets[f'{month}|{category.strip()}'] = value.quantize(Decimal('0.01'))

    def budget_status(self, month, category):
        """Return limit, spent, and remaining for a monthly category budget."""
        self._validate_month(month)
        key = f'{month}|{category}'
        if key not in self.budgets:
            raise KeyError('No budget exists for this category and month')
        limit = self.budgets[key]
        spent = self.spending_by_category(month).get(category, Decimal('0.00'))
        return {'limit': limit, 'spent': spent, 'remaining': limit - spent}

    def to_dict(self):
        """Serialize application state for JSON storage."""
        return {'transactions': [t.to_dict() for t in self.transactions],
                'budgets': {key: str(value) for key, value in self.budgets.items()}}

    @classmethod
    def from_dict(cls, data):
        """Restore state while rejecting malformed or unknown entries."""
        if not isinstance(data, dict) or not isinstance(data.get('transactions'), list) or not isinstance(data.get('budgets'), dict):
            raise ValueError('Invalid finance data format')
        return cls([Transaction.from_dict(t) for t in data['transactions']], data['budgets'])
