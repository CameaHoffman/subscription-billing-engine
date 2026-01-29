"""
Domain models for subscription billing.
"""

from enum import Enum
from datetime import date, timedelta

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Subscription:
    """
    Represents a customer's subscription and billing period.
    """
    def __init__(self, customer_id: str, start_date: date, plan_id: str):
        self.status = SubscriptionStatus.INACTIVE
        self.customer_id = customer_id
        self.start_date = start_date
        self.plan_id = plan_id
        self.current_period_start_date = start_date
        self.current_period_end_date = self.current_period_start_date + timedelta(days=30)
