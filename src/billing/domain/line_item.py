"""
Domain models for line items (individual items) on an invoice.
"""

from decimal import Decimal


class LineItem:
    """
    Represents an billing item from a line on a client invoice.
    """

    def __init__(self, description: str, amount: Decimal, quantity: int = 1):
        
        self.description = description
        self.amount = amount
        self.quantity = quantity
    
    @property
    def subtotal(self):
        return self.amount * self.quantity
    
    def __str__(self):
        return f"Your {self.description} is ${self.amount:.2f} x {self.quantity}, with a subtotal of ${self.subtotal:.2f}."
