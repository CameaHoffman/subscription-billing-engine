from datetime import date
from decimal import Decimal
from billing.domain.invoice import Invoice, InvoiceStatus
from billing.domain.line_item import LineItem
from billing.domain.customer import Customer

def test_invoice_created_with_correct_data():
    
    customer = Customer(email="example@email.com")

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer_id = customer.customer_id,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        line_items=[
            LineItem(
                description="plan",
                amount=Decimal("120.00"),
                quantity=1
            )
        ]
                      )
    
    assert invoice.invoice_id == "invoice_123"
    assert invoice.customer_id == customer.customer_id
    assert invoice.total == Decimal("120.00")
    assert invoice.period_start == date(2026, 1, 1)
    assert invoice.period_end == date(2026, 1, 31)
    assert invoice.status == InvoiceStatus.UNPAID
    assert len(invoice.line_items) == 1

def test_invoice_accepts_line_items():
    item_1 = LineItem(
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    item_2 = LineItem(
        description= "additional plan charge",
        amount=Decimal("10.00"),
        quantity=3
    )

    customer = Customer(email="example@email.com")

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer_id = customer.customer_id,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        line_items = [item_1, item_2],
                      )
    
    assert invoice.line_items == [item_1, item_2]

def test_invoice_total_is_sum_of_line_subtotals():
    item_1 = LineItem(
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    item_2 = LineItem(
        description= "additional plan charge",
        amount=Decimal("10.00"),
        quantity=3
    )

    customer = Customer(email="example@email.com")

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer_id = customer.customer_id,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        line_items = [item_1, item_2],
    )
        
    assert invoice.total == Decimal("130.00")


