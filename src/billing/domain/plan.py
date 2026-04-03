"""
Domain models for subscription plans.
"""
from decimal import Decimal
from uuid import UUID

class Plan:
    """
    Represents a customer's subscription plan.
    """
    def __init__(
            self,
            plan_id: UUID,
            plan_name: str,
            period_days: int,
            amount: Decimal
            ):
        
        if period_days <= 0:
            raise ValueError("period_days must be a positive integer")
        
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.period_days = period_days
        self.amount = amount

    