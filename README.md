# Subscription Billing Engine

A domain-focused subscription billing simulator built to model real-world billing logic and lifecycle rules.

This project isolates business logic from infrastructure and demonstrates how subscription systems handle billing periods, cancellation semantics, invoice generation, and identity management.

---

## Core Concepts

The system models four primary domain entities:

### Customer
- UUID-based identity
- Email address
- Optional name fields
- Auto-generated UTC `created_at` timestamp

### Plan
- `plan_id`
- Billing period length (`period_days`)
- Recurring amount

### Subscription
- References a `Customer` by UUID
- Tracks billing period start and end
- Maintains lifecycle state:
  - `INACTIVE`
  - `ACTIVE`
- Supports:
  - Cancel at period end
  - Immediate cancellation
- Prevents duplicate billing within the same period

### Invoice
- References `Customer` by UUID
- Billing period start and end
- Line items
- Computed total
- Default status: `UNPAID`

### LineItem
- Description
- Amount
- Quantity
- Subtotal calculation

---

## Implemented Business Rules

- Monthly billing cycles
- Invoice generation only when subscription is `ACTIVE`
- Idempotent invoice generation per billing period
- Cancel at period end:
  - Current period still bills
  - Future periods do not
- Immediate cancellation:
  - Subscription becomes inactive immediately
- Invoice totals are derived from line items

---

## Architecture

The project follows a layered domain-first structure:

```
src/
  billing/
    domain/
      customer.py
      plan.py
      subscription.py
      invoice.py
      line_item.py
      billingengine.py
```

- `domain/` contains pure business logic
- No database
- No framework dependencies
- Fully unit-tested

This keeps billing logic isolated and easy to extend.

---

## Testing

- Pytest-based test suite
- Explicit rule-based tests
- Edge case coverage (inactive subscriptions, duplicate billing, cancellation timing)
- 99% test coverage across domain logic

Tests are written to read like requirements and validate business behavior rather than implementation details.

---

## Example Flow

1. Create a `Customer`
2. Create a `Plan`
3. Create a `Subscription`
4. Activate subscription
5. Generate invoice for billing period
6. Cancel subscription (immediate or end-of-period)

---

## Design Decisions

- UUID-based identity across all domain models
- Timezone-aware timestamps (UTC)
- Explicit cancellation methods (no boolean overloads)
- Idempotent billing protection using tracked billing periods
- Business logic isolated from persistence and API layers

---

## Future Enhancements (Roadmap)

- Trial periods and automatic conversion
- Mid-cycle plan upgrades/downgrades with proration
- Credit and refund system
- Ledger / audit trail model
- Event-driven billing service layer
- Persistence layer (SQL or repository abstraction)
- API or CLI interface

---

## How to Run Tests

```
pytest --cov=src --cov-report=term-missing
```

---

## Why This Project

Subscription billing systems are deceptively complex.  
This project focuses on modeling the business rules clearly, testing them thoroughly, and keeping the architecture clean and extensible.


---
Created by Camea Hoffman

