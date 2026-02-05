"""
Domain models for subscription billing.
"""

from enum import Enum
from datetime import date, timedelta
from billing.domain.plan import Plan

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Subscription:
    """
    Represents a customer's subscription and billing period.
    """
    def __init__(self, customer_id: str, start_date: date, plan: Plan):
        self.status = SubscriptionStatus.INACTIVE
        self.customer_id = customer_id
        self.start_date = start_date
        
        self.plan = plan
        self.plan_id = plan.plan_id

        self.current_period_start_date = start_date
        self.current_period_end_date = (
            self.current_period_start_date + timedelta(days=self.plan.period_days)
        )
        
        self.cancel_at_period_end = False
        
    def is_active(self, on_date: date | None = None) -> bool:
        on_date = on_date or date.today()
        return self.start_date <= on_date <= self. current_period_end_date
    
    def advance_to(self, on_date: date) -> None:
    
        if on_date < self.start_date:
            return
        
        while on_date > self.current_period_end_date:
            if self.cancel_at_period_end:
                return

            self.current_period_start_date = self.current_period_end_date + timedelta(days=1)
            self.current_period_end_date = self.current_period_start_date + timedelta(days=30)
            
    def cancel(self):
        self.cancel_at_period_end = True

