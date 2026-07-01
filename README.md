# Subscription Billing Engine

> **🚧 SQL Migration in Progress**
>
> I'm currently migrating this project from an in-memory domain model to a layered architecture with SQLite persistence. The migration is being completed incrementally through small, test-driven commits to demonstrate software design, repository patterns, SQL integration, and test-driven development.

## Current Progress

* ✅ SQLite database schema
* ✅ Customer repository + tests
* ✅ Plan repository + tests
* 🚧 Subscription repository + tests (in progress)
* ⏳ Invoice repository
* ⏳ Line Item repository
* ⏳ Service layer
* ⏳ FastAPI API layer

> **Note:** This project is intentionally developed through small, incremental commits to demonstrate Python proficiency, software design, repository patterns, SQL integration, and test-driven development. AI has been used as a design discussion partner rather than a code generator.

---

A domain-first subscription billing engine built to model real-world billing systems while demonstrating clean architecture, separation of concerns, and test-driven development.

The project separates business logic from persistence, making the domain layer independent of infrastructure and allowing the application to evolve from an in-memory model into a production-style backend architecture.

---

# Core Concepts

The system models five primary domain entities.

## Customer

* UUID-based identity
* Email address
* Optional name fields
* UTC `created_at` timestamp

## Plan

* UUID-based identity
* Billing period length (`period_days`)
* Recurring billing amount

## Subscription

* References a Customer
* References a Plan
* Billing start date
* Optional end date
* Lifecycle status (`active`, `canceled`)
* Supports immediate or scheduled cancellation through domain behavior
* Designed to preserve historical subscription records rather than deleting them

## Invoice

* References a Customer
* Billing period
* Line items
* Computed total
* Default status of `UNPAID`

## Line Item

* Description
* Amount
* Quantity
* Calculated subtotal

---

# Business Rules

Current business rules include:

* Monthly recurring billing
* Invoice generation only for active subscriptions
* One invoice per subscription per billing period
* Immediate cancellation
* End-of-period cancellation
* Invoice totals derived from line items
* UUID identity across all entities

---

# Architecture

The project follows a layered architecture.

```text
API Layer (planned)
        ↓
Service Layer (planned)
        ↓
Domain Layer
        ↓
Repository / Persistence Layer
        ↓
SQLite Database
```

Current project structure:

```text
src/
└── billing/
    ├── domain/
    ├── repos/
    ├── database/
    └── tests/
```

### Domain Layer

Contains pure business logic.

* No SQL
* No framework dependencies
* Business rules only

### Repository Layer

Implements the Repository pattern for persistence.

Repositories are responsible only for:

* Creating records
* Retrieving records
* Listing records
* Updating persisted state

Business decisions remain inside the domain layer.

Current repositories:

* Customer Repository
* Plan Repository
* Subscription Repository (in progress)

---

# Persistence

The project is currently being migrated to SQLite.

The persistence layer maps domain objects to relational tables while maintaining a clear separation between business logic and storage.

Current tables include:

* Customers
* Plans
* Subscriptions

Invoice and Line Item persistence is currently under development.

---

# Testing

The project is developed using test-driven development.

Current testing includes:

* Pytest
* Repository CRUD tests
* Domain behavior tests
* Validation testing
* Edge cases
* Database persistence testing

Tests are designed to validate business behavior rather than implementation details.

---

# Example Workflow

1. Create a Customer
2. Create a Plan
3. Create a Subscription
4. Activate the subscription
5. Generate invoices for billing periods
6. Cancel the subscription
7. Preserve billing history

---

# Design Principles

* Domain-first architecture
* Separation of concerns
* Repository pattern
* Test-driven development
* UUID-based identities
* Explicit domain behavior over CRUD-centric design
* Incremental, commit-driven development
* Extensible architecture for future APIs and services

---

# Roadmap

Planned enhancements include:

* Invoice repository
* Line Item repository
* Billing service layer
* FastAPI REST API
* Background billing scheduler
* Trial periods
* Plan upgrades and downgrades
* Proration support
* Credits and refunds
* Audit logging
* Docker deployment

---

# Running Tests

```bash
pytest --cov=src --cov-report=term-missing
```

---

# Why This Project

Subscription billing systems are deceptively complex.

This project explores how to model billing domains using clean architecture principles while demonstrating object-oriented design, repository patterns, SQL persistence, and test-driven development.

Rather than focusing only on CRUD operations, the project emphasizes modeling business behavior and keeping domain logic independent from infrastructure.

---

Created by **Camea Hoffman**
