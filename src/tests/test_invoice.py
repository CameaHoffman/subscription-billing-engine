from datetime import date
from decimal import Decimal
from billing.domain.invoice import Invoice, InvoiceStatus

def test_invoice_created_with_correct_data():
    invoice = Invoice(
        invoice_id = "invoice_123",
        customer_id = "customer_123",
        amount = Decimal("120.00"),
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
                      )
    
    assert invoice.invoice_id == "invoice_123"
    assert invoice.customer_id == "customer_123"
    assert invoice.amount == Decimal("120.00")
    assert invoice.period_start == date(2026, 1, 1)
    assert invoice.period_end == date(2026, 1, 31)
    assert invoice.status == InvoiceStatus.UNPAID