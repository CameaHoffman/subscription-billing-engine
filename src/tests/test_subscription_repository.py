import pytest
from decimal import Decimal
from datetime import date
from uuid import uuid4
from billing.repos.subscription_repository import SQLiteSubscriptionRepository
from billing.repos.customer_repository import SQLiteCustomerRepository
from billing.repos.plan_repository import SQLitePlanRepository

# CRUD tests for subscription repository

# ------ CREATE SUBSCRIPTION TESTS ------

def test_create_subscription_success(setup_test_db):

    customer_repo = SQLiteCustomerRepository()
    plan_repo = SQLitePlanRepository()
    subscription_repo = SQLiteSubscriptionRepository()

    customer = customer_repo.create(email="test@example.com")

    plan = plan_repo.create(plan_name="Monthly",
                            period_days=30,
                            amount=Decimal("30.00"))
    
    subscription = subscription_repo.create(
        customer_id=customer.customer_id,
        start_date=date.today(),
        plan_id=plan.plan_id,
    )

    assert subscription.customer_id is not None
    assert subscription.customer_id == customer.customer_id
    assert subscription.start_date == date.today()
    assert subscription.plan_id == plan.plan_id

def test_create_subscription_invalid_customer_id(setup_test_db):

    subscription_repo = SQLiteSubscriptionRepository()
    plan_repo = SQLitePlanRepository()

    plan = plan_repo.create(plan_name="Monthly",
                            period_days=30,
                            amount=Decimal("30.00"))

    with pytest.raises(ValueError):
        subscription_repo.create(
            customer_id="",
            start_date=date.today(),
            plan_id=plan.plan_id,
            )
        
def test_create_subscription_customer_id_not_found(setup_test_db):

    subscription_repo = SQLiteSubscriptionRepository()
    plan_repo = SQLitePlanRepository()

    plan = plan_repo.create(plan_name="Monthly",
                            period_days=30,
                            amount=Decimal("30.00"))

    with pytest.raises(ValueError):
        subscription_repo.create(
            customer_id=uuid4(),
            start_date=date.today(),
            plan_id=plan.plan_id,
            )

def test_create_subscription_invalid_plan_id(setup_test_db):
    subscription_repo = SQLiteSubscriptionRepository()
    customer_repo = SQLiteCustomerRepository()
    plan_repo = SQLitePlanRepository()

    customer = customer_repo.create(email="test@example.com")

    plan_repo.create(plan_name="Monthly",
                     period_days=30,
                     amount=Decimal("30.00"))

    with pytest.raises(ValueError):
        subscription_repo.create(
            customer_id=customer.customer_id,
            start_date=date.today(),
            plan_id="",
            )
        
def test_create_subscription_plan_id_not_found(setup_test_db):

    subscription_repo = SQLiteSubscriptionRepository()
    customer_repo = SQLiteCustomerRepository()
    plan_repo = SQLitePlanRepository()

    customer = customer_repo.create(email="test@example.com")

    plan_repo.create(plan_name="Monthly",
                     period_days=30,
                     amount=Decimal("30.00"))

    with pytest.raises(ValueError):
        subscription_repo.create(
            customer_id=customer.customer_id,
            start_date=date.today(),
            plan_id=uuid4(),
            )

