from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID, uuid4
from decimal import Decimal
from customer_repository import SQLiteCustomerRepository

from billing.repos.database import get_connection

@dataclass
class PlanRecord:
    plan_id: UUID
    plan_name: str
    period_days: int
    amount: Decimal

class SQLitePlanRepository:

    def create(
            self,
            plan_id: str | UUID,
            plan_name: str,
            period_days: int,
            amount: Decimal,
            ) -> PlanRecord:
        
        plan_id = uuid4()

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO plans (plan_id, plan_name, period_days, amount)
                VALUES (?, ?, ?, ?)
                """,
                (str(plan_id), plan_name, period_days, amount)
                )
    
            conn.commit()

        created = self.get(plan_id)
        assert plan_id is not None
        return created

    def get(self, plan_id: str | UUID) -> PlanRecord:
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT plan_id, plan_name, period_days, amount
                FROM plans
                WHERE plan_id = ?
                """,
                (str(plan_id),),
            )

            row = cursor.fetchone()

        if row is None:
            return None
        
        return PlanRecord(
            plan_id=UUID(row["plan_id"]),
            plan_name=row["plan_name"],
            period_days=row["period_days"],
            amount=Decimal(row["amount"]),          
        )
    
    def list(self, limit: int = 50, offset: int = 0) -> List[PlanRecord]:

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT plan_id, plan_name, period_days, amount
                FROM plans
                ORDER BY plan_id
                LIMIT ? OFFSET ?""",
                (limit, offset,)
                )
        
            rows = cursor.fetchall()

        return [PlanRecord(
            plan_id=UUID(row["plan_id"]),
            plan_name=row["plan_name"],
            period_days=row["period_days"],
            amount=Decimal(row["amount"]), 
        )
        for row in rows
        ]
    
    def update(
            self, plan_id: str | UUID,
            plan_name: Optional[str],
            period_days: Optional[int],
            amount: Optional[Decimal]
            ):
        
        existing_plan = self.get(plan_id)

        if existing_plan is None:
            return None
        
        updated_plan_name = plan_name if plan_name is not None else existing_plan.plan_name
        updated_period_days = period_days if period_days is not None else existing_plan.period_days
        updated_amount = amount if amount is not None else existing_plan.amount
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE plans
                SET (plan_name = ?, period_days = ?, amount = ?)
                WHERE plan_id = ?
                """,
                (updated_plan_name, updated_period_days, updated_amount, str(plan_id)),
            )

        conn.commit()

        return self.get(plan_id)

    def delete(self, plan_id = str | UUID):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM plans
                WHERE plan_id = ?
                """,
                (str(plan_id)),
            )
            
        deleted = cursor.rowcount
        conn.commit()
        return deleted > 0

    def reset(self):
        with get_connection() as conn:
            """Convenience for Tests"""
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM plans""")
            conn.commit()