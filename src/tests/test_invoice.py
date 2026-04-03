from datetime import date
from decimal import Decimal
from uuid import uuid4
from billing.domain.invoice import Invoice, InvoiceStatus
from billing.domain.line_item import LineItem
from billing.domain.customer import Customer

def test_invoice_created_with_correct_data():
    
    customer = Customer(email="example@email.com")
    expected_plan_id = uuid4()

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer = customer,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        plan_id=expected_plan_id,
        plan_name="basic",
        line_items=[
            LineItem(
                line_item_id="line_item_123",
                description="plan",
                amount=Decimal("120.00"),
                quantity=1
            )
        ]
        )
    
    assert invoice.line_items[0].line_item_id == "line_item_123"
    assert invoice.invoice_id == "invoice_123"
    assert invoice.plan_id == expected_plan_id
    assert invoice.plan_name == "basic"
    assert invoice.customer_id == customer.customer_id
    assert invoice.total == Decimal("120.00")
    assert invoice.period_start == date(2026, 1, 1)
    assert invoice.period_end == date(2026, 1, 31)
    assert invoice.status == InvoiceStatus.UNPAID
    assert len(invoice.line_items) == 1

def test_invoice_accepts_line_items():
    item_1 = LineItem(
        line_item_id="line_item_123",
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    item_2 = LineItem(
        line_item_id="line_item_456",
        description= "additional plan charge",
        amount=Decimal("10.00"),
        quantity=3
    )

    customer = Customer(email="example@email.com")

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer = customer,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        plan_id=uuid4(),
        plan_name="basic",
        line_items = [item_1, item_2],
                      )
    
    assert invoice.line_items == [item_1, item_2]

def test_invoice_total_is_sum_of_line_subtotals():
    item_1 = LineItem(
        line_item_id="line_item_123",
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    item_2 = LineItem(
        line_item_id="line_item_456",
        description= "additional plan charge",
        amount=Decimal("10.00"),
        quantity=3
    )

    customer = Customer(email="example@email.com")

    invoice = Invoice(
        invoice_id = "invoice_123",
        customer= customer,
        period_start = date(2026, 1, 1),
        period_end = date(2026, 1, 31),
        plan_id=uuid4(),
        plan_name="basic",
        line_items = [item_1, item_2],
    )
        
    assert invoice.total == Decimal("130.00")


