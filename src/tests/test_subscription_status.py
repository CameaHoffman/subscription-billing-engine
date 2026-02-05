from billing.domain.subscription import Subscription, SubscriptionStatus
from billing.domain.plan import Plan
from datetime import date, timedelta
from decimal import Decimal

# ------ Active/Inactive ------

def test_subscription_starts_inactive():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )
    
    sub = Subscription(
        customer_id="cust_123",
        start_date=start,
        plan=plan,
                       )
    assert sub.status == SubscriptionStatus.INACTIVE

def test_subscription_is_active_on_start_date():
    on_date = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123",
        start_date=on_date,
        plan=plan,
        )
    
    assert sub.is_active(on_date) is True

def test_subscription_is_inactive_before_start_date():
    start_date = date(2026, 1, 1)
    on_date = date(2025, 12, 31)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )
    
    sub = Subscription(
        customer_id="cust_123",
        start_date=start_date,
        plan=plan,
        )
    
    assert sub.is_active(on_date) is False

# ------ Customer ID ------

def test_subscription_has_customer_id():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )
    
    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    assert sub.customer_id == "cust_123"

# ------ Plan ID -------

def test_subscription_has_plan_id():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    assert sub.plan_id == "plan_123"

# ------ Start/End Dates -------

def test_subscription_has_start_date():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    assert sub.start_date == start

def test_subscription_has_current_period_start_date():
    start = date(2026, 1 ,1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    assert sub.current_period_start_date == start

def test_subscription_has_current_period_end_date():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )

    assert sub.current_period_end_date == start + timedelta(days=plan.period_days)

# ------ Subscription Cancellation ------

def test_subscription_cancels_at_period_end():
    start = date(2026, 1, 1)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00")
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    sub.cancel()

    assert sub.cancel_at_period_end is True

# ------ Advance To ------

def test_advance_to_does_nothing_before_start_date():
    start = date(2026, 1, 1)
    before_start = date(2025, 12, 15)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123", 
        start_date=start,
        plan=plan,
        )
    
    original_end_date = sub.current_period_end_date

    sub.advance_to(before_start)

    assert sub.current_period_end_date == original_end_date

def test_advance_to_does_nothing_within_current_period():
    start = date(2026, 1, 1)
    day_in_current_period = date(2026, 1, 15)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123",
        start_date=start,
        plan=plan)
    
    original_end_date = sub.current_period_end_date
    
    sub.advance_to(day_in_current_period)

    assert sub.current_period_end_date == original_end_date

def test_advance_to_advances_when_past_period_end():
    start = date(2026, 1, 1)
    day_in_next_period = date(2026, 2, 15)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123",
        start_date=start,
        plan=plan)
    
    new_start_date = sub.current_period_end_date + timedelta(days=1)
    new_end_date = new_start_date + timedelta(days=plan.period_days)
    
    sub.advance_to(day_in_next_period)

    assert sub.current_period_end_date == new_end_date

def test_advance_to_advances_multiple_periods_when_on_date_far_in_future():
    start = date(2026, 1, 1)
    six_months_later = date(2026, 6, 15)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123",
        start_date=start,
        plan=plan)

    sub.advance_to(six_months_later)

    assert sub.current_period_start_date <= six_months_later <= sub.current_period_end_date

def test_advance_to_does_not_extend_past_period_end_when_canceled_at_period_end():
    start = date(2026, 1, 1)
    far_future = date(2026, 6, 15)
    plan = Plan(
        plan_id="plan_123",
        period_days=30,
        amount=Decimal("100.00"),
        )

    sub = Subscription(
        customer_id="cust_123",
        start_date=start,
        plan=plan)
    
    final_end = sub.current_period_end_date
    
    sub.cancel()
    sub.advance_to(far_future)

    assert sub.current_period_end_date == final_end
