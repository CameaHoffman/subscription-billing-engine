# Subscription Billing Engine

A Python-based billing engine that processes subscription lifecycle events and produces invoices, account state and an auditable ledger.

This project focuses on modeling real-world billing rules and edge cases, with business logic isolated from infracstructure and covered by comprehensive tests.

## Goals
- Model subscription and billing behavior accurately
- Handle edge cases beyond "happy paths"
- Keep business logic deterministic and testable

## Core Concepts
- Subscriptions with billing cycles and state transitions
- Event-driven changes (trial start, plan changes, cancellations)
- Invoice generation with line items and totals
- Ledger entries for auditability (credits and debits)

## Tech Stack
- Python
- Domain-driven design (domain models + services)
- pytest (edge-case and regression tests)

## Project STatus 
Early development - starting with core domain models and billing rules.

---
Created by Camea Hoffman

