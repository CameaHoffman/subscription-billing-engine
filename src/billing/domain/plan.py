"""
Domain models for subscription plans.
"""

class Plan:
    """
    Represents a customer's subscription plan.
    """
    def __init__(self, plan_id: str, period_days: int):
        if period_days <= 0:
            raise ValueError("period_days must be a positive integer")

        self.plan_id = plan_id
        self.period_days = period_days

