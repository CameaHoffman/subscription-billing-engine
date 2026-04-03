import pytest
from decimal import Decimal
from uuid import uuid4
from billing.domain.plan import Plan

def test_plan_rejects_non_positive_period_days():
    with pytest.raises(ValueError):
        Plan(
            plan_id=uuid4(),
            plan_name="basic",
            period_days=0,
            amount=Decimal("100.00"),
            )
        
def test_plan_accepts_positive_period_days():
    plan = Plan(
        plan_id=uuid4(),
        plan_name="basic",
        period_days=30,
        amount=Decimal("100.00"),
        )
    assert plan.period_days == 30

