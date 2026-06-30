from dataclasses import dataclass
from uuid import UUID
from datetime import date, timedelta
from repos.customer_repository import SQLiteCustomerRepository
from repos.plan_repository import SQLitePlanRepository

@dataclass
class SubscriptionRecord:
    subscription_id: UUID
    customer_id: UUID
    start_date: date
    plan_id: UUID

# create subscription repository
# CRUD operations
# create subscription
# get subscription
# get subscription list
# update subscription 
# delete subscription
# reset subscription