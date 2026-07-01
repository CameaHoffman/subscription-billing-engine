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

# ------ GET SUBSCRIPTION TESTS ------
def test_get_subscription_success(setup_test_db):
    subscription_repo = SQLiteSubscriptionRepository()
    customer_repo = SQLiteCustomerRepository()
    plan_repo = SQLitePlanRepository()

    customer = customer_repo.create(email="test@example.com")

    plan = plan_repo.create(
        plan_name="Monthly",
        period_days=30,
        amount=Decimal("30.00")
    )

    subscription = subscription_repo.create(
        customer_id=customer.customer_id,
        start_date=date.today(),
        plan_id=plan.plan_id,
        )
    
    result = subscription_repo.get(subscription.subscription_id)
    
    assert result.subscription_id == subscription.subscription_id
    assert result.customer_id == customer.customer_id
    assert result.start_date == subscription.start_date
    assert result.plan_id == plan.plan_id

def test_get_subscription_invalid_subscription_id(setup_test_db):

    subscription_repo = SQLiteSubscriptionRepository()

    with pytest.raises(ValueError):
        subscription_repo.get(subscription_id="")

def test_get_subscription_returns_none_when_subscription_id_not_found(setup_test_db):
    
    subscription_repo = SQLiteSubscriptionRepository()

    result = subscription_repo.get(subscription_id=uuid4())

    assert result is None

# ------ GET SUBSCRIPTION LIST ------

def test_get_subscription_list_success(setup_test_db):

    subscription_repo = SQLiteSubscriptionRepository()
    customer_repo = SQLiteCustomerRepository()
    plan_repo = SQLitePlanRepository()

    customer_1 = customer_repo.create(email="test@example.com")
    customer_2 = customer_repo.create(email="test2@example.com")

    plan = plan_repo.create(plan_name="Monthly",
                                    period_days=30,
                                    amount=Decimal("10.00"))

    subscription_1 = subscription_repo.create(customer_id=customer_1.customer_id,
                                              start_date=date.today(),
                                              plan_id=plan.plan_id
                                              )
    
    subscription_2 = subscription_repo.create(customer_id=customer_2.customer_id,
                                              start_date=date.today(),
                                              plan_id=plan.plan_id)
    
    result = subscription_repo.list()
    subscriptions = [c.subscription_id for c in result]

    assert result is not None
    assert len(result) == 2
    assert set(subscriptions) == {subscription_1.subscription_id,
                                  subscription_2.subscription_id}

def test_get_subscription_list_returns_empty_list(setup_test_db):
    
    subscription_repo = SQLiteSubscriptionRepository()

    result = subscription_repo.list()

    assert result == []

