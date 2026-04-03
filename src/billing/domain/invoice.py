"""
Domain models for client invoicing.
"""
from enum import Enum
from decimal import Decimal
from datetime import date
from typing import Optional, List
from billing.domain.line_item import LineItem
from billing.domain.customer import Customer

class InvoiceStatus(Enum):
    PAID = "paid"
    UNPAID = "unpaid"

class Invoice:
    """
    Represents a customer's invoicing 
    for subscription payments."""
    def __init__(
            self,
            invoice_id: str,
            customer: Customer,
            period_start: date,
            period_end: date,
            plan_id: str,
            plan_name: str,
            status: InvoiceStatus = InvoiceStatus.UNPAID,
            line_items: Optional[List[LineItem]] = None,
            ):
        
        self.customer = customer
        self.customer_id = customer.customer_id
        self.invoice_id = invoice_id
        self.period_start = period_start
        self.period_end = period_end
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.status = status
        self.line_items = line_items or []

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.line_items), Decimal("0.00"))
    
    @property
    def amount(self) -> Decimal:
        return self.total