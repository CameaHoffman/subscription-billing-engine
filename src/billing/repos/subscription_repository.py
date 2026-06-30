from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import date

from billing.repos.database import get_connection
from billing.repos.customer_repository import SQLiteCustomerRepository
from billing.repos.plan_repository import SQLitePlanRepository

@dataclass
class SubscriptionRecord:
    subscription_id: UUID
    customer_id: UUID
    start_date: date
    plan_id: UUID

class SQLiteSubscriptionRepository:
    def create(
            self,
            customer_id: str,
            start_date: date,
            plan_id: str,
            ) -> SubscriptionRecord:

        if not customer_id:
            raise ValueError("Invalid customer ID.")
        
        customer_repo = SQLiteCustomerRepository()
        customer = customer_repo.get(customer_id)
        
        if customer is None:
            raise ValueError("Customer ID not found.")
        
        if not plan_id:
            raise ValueError("Invalid plan ID.")
        
        plan_repo = SQLitePlanRepository()
        plan = plan_repo.get(plan_id)
        
        if plan is None:
            raise ValueError("Subscription not possible without a plan ID.")

        subscription_id=uuid4()

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO subscriptions (subscription_id, customer_id, start_date, plan_id)
                VALUES (?, ?, ?, ?)
                """,
                (str(subscription_id), str(customer_id), start_date.isoformat(), str(plan_id))
                )
            
            conn.commit()
        
        created = self.get(subscription_id)

    #TO-DO: REPLACE ASSERT WITH ERROR HANDLING
    
        assert created is not None
        return created

    def get(
            self, 
            subscription_id: UUID | str, 
            ) -> SubscriptionRecord | None:
        
        if not subscription_id:
            raise ValueError("Invalid subscription ID.")
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT subscription_id, customer_id, start_date, plan_id
                FROM subscriptions
                WHERE subscription_id = ?
                """,
                (str(subscription_id),)
                )
            
            row = cursor.fetchone()

            if row is None:
                return None

            return SubscriptionRecord(
                subscription_id= UUID(row["subscription_id"]),
                customer_id = UUID(row["customer_id"]),
                start_date= date.fromisoformat(row["start_date"]),
                plan_id= UUID(row["plan_id"]),
            )

    def list():
        pass

    def update():
        pass

    def delete():
        pass

    def reset():
        pass
