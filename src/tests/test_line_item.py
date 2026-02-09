from billing.domain.line_item import LineItem
from decimal import Decimal

def test_line_item_stores_single_item_from_invoice():

    line_item = LineItem(
        description= "Plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    assert line_item.description == "Plan charge"
    assert line_item.amount == Decimal("100.00")
    assert line_item.quantity == 1

def test_line_item_calculates_subtotal():
    
    line_item = LineItem(
        description= "Plan charge",
        amount=Decimal("100.00"),
        quantity=3
    )

    assert line_item.subtotal == Decimal("300.00")