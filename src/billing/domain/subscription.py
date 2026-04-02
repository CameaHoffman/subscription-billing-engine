"""
Domain models for subscription billing.
"""

from enum import Enum
from datetime import date, timedelta
from billing.domain.plan import Plan
from billing.domain.customer import Customer
from uuid import UUID

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Subscription:
    """
    Represents a customer's subscription and billing period.
    """
    def __init__(
            self,
            subscription_id: UUID,
            customer: Customer,
            start_date: date,
            plan: Plan,
            invoiced_periods: set[date] | None = None
            ):
        
        self.subscription_id = subscription_id or uuid4()
        
        self.status = SubscriptionStatus.INACTIVE

        self.customer = customer
        self.customer_id = customer.customer_id
        self.start_date = start_date
        
        self.plan = plan
        self.plan_id = plan.plan_id

        self.current_period_start_date = start_date
        self.current_period_end_date = (
            self.current_period_start_date + timedelta(days=self.plan.period_days)
        )
        
        self.cancel_at_period_end = False

        self.invoiced_periods = invoiced_periods or set()
        
    def is_active(self, on_date: date | None = None) -> bool:
        on_date = on_date or date.today()
        return self.start_date <= on_date <= self. current_period_end_date
    
    def advance_to(self, on_date: date) -> None:
    
        if on_date < self.start_date:
            return
        
        while on_date > self.current_period_end_date:
            if self.cancel_at_period_end:
                return

            self.current_period_start_date = self.current_period_end_date
            self.current_period_end_date = self.current_period_start_date + timedelta(days=self.plan.period_days)
            
    def cancel(self):
        self.cancel_at_period_end = True

    def cancel_immediately(self, canceled_at: date):
        self.status = SubscriptionStatus.INACTIVE
        self.current_period_end_date = canceled_at
        self.cancel_at_period_end = False

