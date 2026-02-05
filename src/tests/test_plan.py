import pytest
from billing.domain.plan import Plan

def test_plan_rejects_non_positive_period_days():
    with pytest.raises(ValueError):
        Plan(plan_id="plan_123",
             period_days=0)
        
def test_plan_accepts_positive_period_days():
    plan = Plan(plan_id="plan_123",
                period_days=30)
    assert plan.period_days == 30

