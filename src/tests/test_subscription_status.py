from billing.domain.subscription import Subscription, SubscriptionStatus

def test_subscription_starts_inactive():
    sub = Subscription(customer_id="cust_123")
    assert sub.status == SubscriptionStatus.INACTIVE

def test_subscription_has_customer_id():
    sub = Subscription(customer_id="cust_123")
    assert sub.customer_id == "cust_123"