"""
Domain models for generating client invoices.
"""

from datetime import date
from typing import Optional
from uuid import uuid4
from billing.domain.invoice import Invoice
from billing.domain.subscription import Subscription, SubscriptionStatus
from billing.domain.line_item import LineItem

class BillingEngine:
    """
    Decides whether an invoice should be generated for a subscription.
    """

    def generate_invoice(self, subscription: Subscription, as_of_date: date) -> Optional[Invoice]:
        if subscription.status != SubscriptionStatus.ACTIVE:
            return None
        
        subscription.advance_to(as_of_date)
        
        if not (subscription.current_period_start_date <= as_of_date <= subscription.current_period_end_date):
            return None

        return Invoice(
            invoice_id="inv_123", # temporary placeholder until invoice persistence is implemented
            customer=subscription.customer,
            period_start=subscription.current_period_start_date,
            period_end=subscription.current_period_end_date,
            plan_id=subscription.plan_id,
            plan_name=subscription.plan_name,
            line_items=[
                LineItem(
                    line_item_id=str(uuid4()),
                    description="plan charge",
                    amount=subscription.plan.amount,
                    quantity=1
                    )
            ]
        )


