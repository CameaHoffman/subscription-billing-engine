"""
Domain models for client invoicing.
"""
from enum import Enum
from datetime import date
from decimal import Decimal
from billing.domain.line_item import LineItem

class InvoiceStatus(Enum):
    PAID = "paid"
    UNPAID = "unpaid"

class Invoice:
    """
    Represents a customer's invoicing 
    for subscription payments."""
    def __init__(self,
                 invoice_id: str,
                 customer_id: str,
                 amount: Decimal,
                 period_start: date,
                 period_end: date,
                 status: InvoiceStatus = InvoiceStatus.UNPAID,
                 line_items = None
                 ):
        
        self.invoice_id = invoice_id
        self.customer_id = customer_id
        self.amount = amount
        self.period_start = period_start
        self.period_end = period_end
        self.status = status
        self.line_items = line_items or []

