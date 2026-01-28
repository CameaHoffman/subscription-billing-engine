from billing.domain.subscription import Subscription, SubscriptionStatus

def test_subscription_starts_inactive():
    sub = Subscription()
    assert sub.status == SubscriptionStatus.INACTIVE