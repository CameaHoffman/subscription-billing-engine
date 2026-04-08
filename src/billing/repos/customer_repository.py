from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from billing.repos.database import get_connection

@dataclass
class CustomerRecord:
    email: str
    customer_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None

class SQLiteCustomerRepository:

    def create(
            self,
            email: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            ) -> CustomerRecord:
        
        if not email:
            raise ValueError("Email is required.")
        
        customer_id = uuid4()

        with get_connection() as conn:
            cursor = conn.cursor()
        
            cursor.execute(
                """INSERT INTO customers (customer_id, email, first_name, last_name)
                VALUES (?, ?, ?, ?)""",
                (str(customer_id), email, first_name, last_name)
            )

            conn.commit()

        created = self.get(customer_id)
        assert created is not None
        return created
    
    def get(self, customer_id: str | UUID) -> Optional[CustomerRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT customer_id, email, first_name, last_name 
                FROM customers 
                WHERE customer_id = ?""",
                (str(customer_id),),
            )
            row = cursor.fetchone()

        if row is None:
            return None
        
        return CustomerRecord(
            customer_id=UUID(row["customer_id"]),
            email=row["email"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            )
        
    def get_customer_by_email(self, email: str) -> Optional[CustomerRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT customer_id, email, first_name, last_name
                FROM customers
                WHERE email = ?""",
                (email,)
            )

            row = cursor.fetchone()

        if row is None:
            return None
        
        return CustomerRecord(
            customer_id=UUID(row["customer_id"]),
            email=row["email"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            )
    
    def list(self, limit: int = 50, offset: int = 0) -> List[CustomerRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT customer_id, email, first_name, last_name
                FROM customers
                ORDER BY customer_id
                LIMIT ? OFFSET ?""",
                (limit, offset)
            )
            rows = cursor.fetchall()

        return [
            CustomerRecord(
                customer_id=UUID(row["customer_id"]),
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"]
            )
            for row in rows
        ]
    
    def update(
            self,
            customer_id: str | UUID,
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None) -> Optional[CustomerRecord]:
        
        existing_customer = self.get(customer_id)

        if existing_customer is None:
            return None
        
        updated_first_name = first_name if first_name is not None else existing_customer.first_name
        updated_last_name = last_name if last_name is not None else existing_customer.last_name
        updated_email = email if email is not None else existing_customer.email
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE customers
                SET email = ?, first_name = ?, last_name = ?
                WHERE customer_id = ?
                """,
                (updated_email, updated_first_name, updated_last_name, str(customer_id)),
            )
            conn.commit()
            
        return self.get(customer_id)
    
    def delete(self, customer_id: str | UUID) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM customers WHERE customer_id = ?",
                (str(customer_id),)
            )
        
            deleted = cursor.rowcount
            conn.commit()

        return deleted > 0

    def reset(self) -> None:
        """ Convenience for tests."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers")
            conn.commit()