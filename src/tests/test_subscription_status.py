from billing.domain.subscription import Subscription, SubscriptionStatus
from datetime import date, timedelta

def test_subscription_starts_inactive():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", start_date=start)
    assert sub.status == SubscriptionStatus.INACTIVE

def test_subscription_has_customer_id():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", start_date=start)
    assert sub.customer_id == "cust_123"

def test_subscription_has_start_date():
    start = date(2026, 1, 1)
    sub = Subscription(customer_id="cust_123", start_date=start)
    assert sub.start_date == start