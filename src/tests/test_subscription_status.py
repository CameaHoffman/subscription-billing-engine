from billing.domain.subscription import Subscription, SubscriptionStatus
from datetime import date, timedelta

def test_subscription_starts_inactive():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )
    assert sub.status == SubscriptionStatus.INACTIVE

def test_subscription_has_customer_id():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )
    assert sub.customer_id == "cust_123"

def test_subscription_has_start_date():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )
    assert sub.start_date == start

def test_subscription_has_plan_id():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )
    assert sub.plan_id == "plan_123"

def test_subscription_has_current_period_start_date():
    start = date(2026, 1 ,1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
    )
    
    assert sub.current_period_start_date == start

def test_subscription_has_current_period_end_date():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )

    assert sub.current_period_end_date == start + timedelta(30)

def test_subscription_cancels_at_period_end():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", 
                       start_date=start,
                       plan_id="plan_123",
                       )
    sub.cancel()

    assert sub.cancel_at_period_end is True