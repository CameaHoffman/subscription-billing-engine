from enum import Enum

class Subscription:
    def __init__(self, customer_id: str):
        self.status = SubscriptionStatus.INACTIVE
        self.customer_id = customer_id
        
class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
