from enum import Enum

class Subscription:
    def __init__(self):
        self.status = SubscriptionStatus.INACTIVE

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
