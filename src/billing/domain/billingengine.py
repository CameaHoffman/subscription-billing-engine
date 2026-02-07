"""
Domain models for generating client invoices.
"""

from datetime import date
from typing import Optional
from billing.domain.invoice import Invoice, InvoiceStatus
from billing.domain.subscription import Subscription, SubscriptionStatus

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
        
        period_key = subscription.current_period_start_date

        if period_key in subscription.invoiced_periods:
            return None

        subscription.invoiced_periods.add(period_key)

        return Invoice(
            invoice_id="inv_123", # invoice_id will be assigned by persistence layer later
            customer_id=subscription.customer_id,
            amount=subscription.plan.amount,
            period_start=subscription.current_period_start_date,
            period_end=subscription.current_period_end_date,
        )

