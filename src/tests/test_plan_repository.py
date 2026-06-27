import pytest
from uuid import UUID, uuid4
from decimal import Decimal
from billing.repos.plan_repository import SQLitePlanRepository
from billing.repos.customer_repository import SQLiteCustomerRepository

# CRUD operation tests

# ------ CREATE PLAN TESTS ------

def test_create_plan_success(setup_test_db):
    
    repo = SQLitePlanRepository()

    plan = repo.create(
        plan_name = "Plan 01",
        period_days = 30,
        amount = Decimal("30.00"),
    )

    assert plan.plan_name == "Plan 01"
    assert plan.period_days == 30
    assert plan.amount == Decimal("30.00")
    assert isinstance(plan.plan_id, UUID)

def test_create_plan_failure_missing_plan_name(setup_test_db):
    
    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="",
            period_days=30,
            amount=Decimal("30.00"),
        )

def test_create_plan_failure_plan_name_none(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name=None,
            period_days=30,
            amount=Decimal("30.00"),
        )

def test_create_plan_failure_missing_period_days(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=None,
            amount=Decimal("30.00"),
        )

def test_create_plan_failure_zero_period_days(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=0,
            amount=Decimal("30.00"),
        )

def test_create_plan_failure_negative_period_days(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=-10,
            amount=Decimal("30.00"),
        )


def test_create_plan_failure_missing_amount(setup_test_db):
    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=30,
            amount=None,
        )

def test_create_plan_failure_amount_zero(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=30,
            amount=Decimal("0.00"),
        )

def test_create_plan_failure_amount_negative(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.create(
            plan_name="Plan 1",
            period_days=30,
            amount=Decimal("-10.00"),
        )

# ------ GET PLAN TESTS ------

def test_get_plan_success():

    pass

def test_get_plan_failure_invalid_plan_id():
    pass

def test_get_plan_empty_field_returns_none():
    pass

# ------ GET PLAN LIST TESTS ------

def test_get_plan_list_sucess():
    pass

def test_get_plan_returns_empty_list():
    pass

# ------ PATCH/UPDATE PLAN TESTS ------
def test_plan_update_success():
    pass

def test_plan_update_failure_invalid_plan_id():
    pass

def test_plan_update_failure_invalid_plan_name():
    pass

def test_plan_update_failure_invalid_period_days():
    pass

def test_plan_update_failure_invalid_amount():
    pass


# ------ DELETE PLAN TESTS ------

def test_delete_plan_success():
    pass

def test_delete_plan_not_found():
    pass

def test_delete_plan_twice():
    pass
