"""
Domain models for subscription plans.
"""
from decimal import Decimal

class Plan:
    """
    Represents a customer's subscription plan.
    """
    def __init__(self, plan_id: str, period_days: int, amount: Decimal):
        if period_days <= 0:
            raise ValueError("period_days must be a positive integer")
        
        self.plan_id = plan_id
        self.period_days = period_days
        self.amount = amount

    