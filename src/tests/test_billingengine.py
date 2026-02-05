from datetime import date
from decimal import Decimal
from billing.domain.invoice import Invoice
from billing.domain.subscription import Subscription, SubscriptionStatus
from billing.domain.plan import Plan
from billing.domain.billingengine import BillingEngine

def test_billingengine_generates_invoice_from_current_subscription_billing_period():
    start_date = date(2026, 1, 1)
    billing_date = date(2026, 1, 15)

    plan = Plan(plan_id="plan_123", period_days=30, amount=Decimal("100.00"))

    sub = Subscription(
        customer_id="cust_123",
        start_date=start_date,
        plan=plan,
        )
    
    sub.status = SubscriptionStatus.ACTIVE

    engine = BillingEngine()

    invoice = engine.generate_invoice(subscription=sub, as_of_date=billing_date)
    
    assert isinstance(invoice, Invoice)
    assert invoice.customer_id == "cust_123"
    assert invoice.amount == plan.amount
    assert invoice.period_start == sub.current_period_start_date
    assert invoice.period_end == sub.current_period_end_date