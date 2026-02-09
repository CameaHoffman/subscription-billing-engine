from billing.domain.line_item import LineItem
from decimal import Decimal

def test_line_item_stores_single_item_from_invoice():

    item = LineItem(
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    assert item.description == "plan charge"
    assert item.amount == Decimal("100.00")
    assert item.quantity == 1

def test_line_item_calculates_subtotal():
    
    item = LineItem(
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=3
    )

    assert item.subtotal == Decimal("300.00")

def test_line_item_returns_str():

    item = LineItem(
        description= "plan charge",
        amount=Decimal("100.00"),
        quantity=3
    )

    assert str(item) == "Your plan charge is $100.00 x 3, with a subtotal of $300.00."