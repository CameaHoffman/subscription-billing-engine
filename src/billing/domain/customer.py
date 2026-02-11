from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

class Customer:
    def __init__(
            self,
            email: str,
            customer_id: Optional[UUID] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            created_at: Optional[datetime] = None,
            ):
        
        self.customer_id = customer_id or uuid4()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at or datetime.now(timezone.utc)