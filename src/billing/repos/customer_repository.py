from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from repos.database import get_connection

@dataclass
class CustomerRecord:
    email: str
    customer_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None

class SQLiteCustomerRepository():

    def create(
            self,
            email: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None
            ) -> CustomerRecord:
        
        customer_id = str(uuid4())

        with get_connection() as conn:
            cursor = conn.cursor()
        
            cursor.execute(
                "INSERT INTO customer (customer_id, email, first_name, last_name) VALUES (?, ?, ?)",
                (email, first_name, last_name)
            )

            customer_id = cursor.lastrowid
        
        return self.get(customer_id)