from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from billing.domain.invoice import Invoice
from billing.domain.subscription import Subscription, SubscriptionStatus
from billing.domain.plan import Plan
from billing.domain.billingengine import BillingEngine
from billing.domain.customer import Customer
from billing.domain.line_item import LineItem

def test_billingengine_generates_invoice_from_current_subscription_billing_period():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 1, 15)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.ACTIVE

    engine = BillingEngine()

    line_item = LineItem(
        line_item_id="line_item_123",
        description="plan charge",
        amount=Decimal("100.00"),
        quantity=1
    )

    invoice = engine.generate_invoice(
        subscription=sub,
        as_of_date=billing_date
        )
    
    assert sub.current_period_start_date in sub.invoiced_periods
    assert isinstance(invoice, Invoice)
    assert isinstance(invoice.customer_id, UUID)
    assert invoice.customer_id == customer.customer_id
    assert invoice.total == plan.amount
    assert len(invoice.line_items) == 1
    assert invoice.line_items[0].amount == plan.amount
    assert invoice.period_start == sub.current_period_start_date
    assert invoice.period_end == sub.current_period_end_date

def test_billingengine_does_not_generate_invoice_on_inactive_subscription():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 2, 15)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.INACTIVE

    engine = BillingEngine()
    
    invoice = engine.generate_invoice(subscription=sub, as_of_date=billing_date)

    assert invoice is None

def test_billingengine_returns_none_on_duplicate_invoice_for_same_period():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 1, 15)
    second_billing_date = date(2026, 1, 16)

    customer = Customer(email="example@email.com")

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.ACTIVE

    engine = BillingEngine()
    
    invoice = engine.generate_invoice(subscription=sub, as_of_date=billing_date)
    invoice_2 = engine.generate_invoice(subscription=sub, as_of_date=second_billing_date)

    assert sub.current_period_start_date in sub.invoiced_periods
    assert isinstance(invoice, Invoice)
    assert invoice_2 is None

def test_billingengine_returns_none_when_as_of_date_outside_billing_period():
    start_date = date(2026, 1, 1)
    outside_date = date(2025, 1, 31)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.ACTIVE

    engine = BillingEngine()
    
    invoice = engine.generate_invoice(subscription=sub, as_of_date=outside_date)

    assert invoice is None
    
def test_billingengine_returns_invoice_in_billing_period_after_cancelling_subscription():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 1, 15)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    sub.status = SubscriptionStatus.ACTIVE
    
    sub.cancel()

    engine = BillingEngine()
    
    invoice = engine.generate_invoice(subscription=sub, as_of_date=billing_date)

    assert isinstance(invoice, Invoice)

def test_billingengine_returns_none_after_cancelled_subscription_reaches_period_end():
    start_date = date(2026, 1, 1)
    future_date = date(2026, 3, 1)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    sub.status = SubscriptionStatus.ACTIVE
    
    sub.cancel()

    engine = BillingEngine()
    
    invoice = engine.generate_invoice(subscription=sub, as_of_date=future_date)

    assert invoice is None

def test_billingengine_generates_invoice_with_single_plan_line_item():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 1, 15)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    customer = Customer(email="example@email.com")

    sub = Subscription(
        subscription_id=uuid4(),
        customer=customer,
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.ACTIVE

    engine = BillingEngine()
    invoice = engine.generate_invoice(subscription=sub, as_of_date=billing_date)

    assert isinstance(invoice, Invoice)
    assert len(invoice.line_items) == 1

    item = invoice.line_items[0]
    assert item.description == "plan charge"
    assert item.amount == Decimal("100.00")
    assert item.quantity == 1

    assert invoice.total == plan.amount
    