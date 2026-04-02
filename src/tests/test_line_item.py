from billing.domain.line_item import LineItem
from uuid import uuid4
from decimal import Decimal

def test_line_id_is_assigned():
    item = LineItem(
        line_item_id=str(uuid4()),
        description="test item",
        amount=Decimal("50.00"),
        quantity = 1
    )

    assert item.line_item_id is not None
    assert isinstance(item.line_item_id, str)
    

def test_line_item_stores_single_item_from_invoice():
    item = LineItem(
        line_item_id = "line_item_123",
        description = "plan charge",
        amount = Decimal("100.00"),
        quantity = 1
    )

    assert item.description == "plan charge"
    assert item.amount == Decimal("100.00")
    assert item.quantity == 1

def test_line_item_calculates_subtotal():   
    item = LineItem(
        line_item_id ="line_item_123",
        description = "plan charge",
        amount = Decimal("100.00"),
        quantity = 3
    )

    assert item.subtotal == Decimal("300.00")

def test_line_item_returns_str():
    item = LineItem(
        line_item_id = "line_item_123",
        description = "plan charge",
        amount = Decimal("100.00"),
        quantity = 3
    )

    assert str(item) == "Your plan charge is $100.00 x 3, with a subtotal of $300.00."

def test_line_item_repr_returns_simple_str_for_developers():
    item = LineItem(
        line_item_id = "line_item_123",
        description = "plan charge",
        amount = Decimal("100.00"),
        quantity = 3
    )

    assert repr(item) == "LineItem(description='plan charge', amount=100.00, quantity=3, subtotal=300.00)"