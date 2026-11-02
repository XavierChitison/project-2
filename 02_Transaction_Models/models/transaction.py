"""Personal Finance Tracker | Author: Xavier Chitison | Date: 2026-10-29.

Purpose: Define validated financial transactions and income/expense subclasses.
Resources: Original implementation; Python standard library and pytest documentation.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Transaction:
    """Represent a validated monetary transaction."""

    amount: Decimal
    category: str
    description: str
    transaction_date: str

    def __post_init__(self):
        """Validate transaction fields and normalize monetary precision."""
        try:
            amount = Decimal(str(self.amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Amount must be a valid number") from exc
        if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
            raise ValueError("Amount must be positive with at most two decimal places")
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("Category cannot be empty")
        if not isinstance(self.description, str):
            raise ValueError("Description must be text")
        try:
            date.fromisoformat(self.transaction_date)
        except (ValueError, TypeError) as exc:
            raise ValueError("Date must use YYYY-MM-DD") from exc
        object.__setattr__(self, 'amount', amount.quantize(Decimal('0.01')))
        object.__setattr__(self, 'category', self.category.strip())

    def signed_amount(self):
        """Return this transaction's contribution to the balance."""
        raise NotImplementedError("Use Income or Expense")

    def to_dict(self):
        """Convert this transaction to a JSON-compatible dictionary."""
        return {'type': type(self).__name__, 'amount': str(self.amount),
                'category': self.category, 'description': self.description,
                'transaction_date': self.transaction_date}

    @classmethod
    def from_dict(cls, data):
        """Restore an income or expense from validated serialized fields."""
        if not isinstance(data, dict):
            raise ValueError('Transaction must be an object')
        kind = {'Income': Income, 'Expense': Expense}.get(data.get('type'))
        if kind is None:
            raise ValueError('Unknown transaction type')
        try:
            return kind(data['amount'], data['category'], data['description'], data['transaction_date'])
        except (KeyError, TypeError) as exc:
            raise ValueError('Transaction is missing required fields') from exc


class Income(Transaction):
    """Represent funds added to the balance."""

    def signed_amount(self):
        """Return the positive income amount."""
        return self.amount


class Expense(Transaction):
    """Represent funds subtracted from the balance."""

    def signed_amount(self):
        """Return the negative expense amount."""
        return -self.amount
