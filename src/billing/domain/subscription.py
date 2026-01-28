from enum import Enum
from datetime import date

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Subscription:
    def __init__(self, customer_id: str, start_date: date, plan_id: str):
        self.status = SubscriptionStatus.INACTIVE
        self.customer_id = customer_id
        self.start_date = start_date
        self.plan_id = plan_id
        

