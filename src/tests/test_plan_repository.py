import pytest
from uuid import UUID, uuid4
from decimal import Decimal
from billing.repos.plan_repository import SQLitePlanRepository

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

def test_get_plan_success(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name = "plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )

    result = repo.get(plan.plan_id)

    assert result is not None
    assert result.plan_id == plan.plan_id
    assert result.plan_name == "plan 01"
    assert result.period_days == 30
    assert result.amount == Decimal("10.00")

def test_get_plan_returns_none_when_plan_not_found(setup_test_db):

    repo = SQLitePlanRepository()

    fake_id = uuid4()

    result = repo.get(fake_id)

    assert result is None 

def test_get_plan_empty_field_returns_error(setup_test_db):
    
    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.get(None)

# ------ GET PLAN LIST TESTS ------

def test_get_plan_list_success(setup_test_db):
    
    repo = SQLitePlanRepository()

    repo.create(plan_name = "plan 01",
                period_days=30,
                amount=Decimal("10.00")
                )
    
    repo.create(plan_name = "plan 02",
                period_days=30,
                amount=Decimal("25.00")
                )

    result = repo.list()
    plan_names = [c.plan_name for c in result]

    assert result is not None
    assert len(result) == 2
    assert set(plan_names) == {"plan 01", "plan 02"}

def test_get_plan_returns_empty_list(setup_test_db):

    repo = SQLitePlanRepository()

    result = repo.list()

    assert result is not None
    assert result == []
    assert len(result) == 0

# ------ PATCH/UPDATE PLAN TESTS ------
def test_plan_update_success(setup_test_db):
     
    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
     
    repo.update(
        plan_id=plan.plan_id,
        plan_name="plan 02")
     
    updated = repo.get(plan.plan_id)

    assert updated is not None
    assert updated.plan_name == "plan 02"
    assert updated.period_days == 30
    assert updated.amount == Decimal("10.00")

def test_plan_update_failure_when_plan_id_is_empty_string(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.update(plan_id="")

def test_plan_update_failure_when_plan_id_is_none(setup_test_db):

    repo = SQLitePlanRepository()

    with pytest.raises(ValueError):
        repo.update(plan_id=None)

def test_plan_update_returns_none_when_plan_not_found(setup_test_db):

    repo = SQLitePlanRepository()

    invalid_plan_id = uuid4()

    result = repo.update(plan_id=invalid_plan_id)

    assert result is None

def test_plan_update_failure_invalid_plan_name(setup_test_db):
    
    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
     
    with pytest.raises(ValueError):

        repo.update(
        plan_id=plan.plan_id,
        plan_name="")

def test_plan_update_failure_when_period_days_zero(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
    
    with pytest.raises(ValueError):
        repo.update(
            plan_id=plan.plan_id,
            plan_name="plan 01",
            period_days=0
        )

def test_plan_update_failure_when_period_days_negative(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
    
    with pytest.raises(ValueError):
        repo.update(
            plan_id=plan.plan_id,
            plan_name="plan 01",
            period_days=-1
        )

def test_plan_update_failure_when_amount_zero(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
    
    with pytest.raises(ValueError):
        repo.update(
            plan_id=plan.plan_id,
            plan_name="plan 01",
            amount=Decimal("0.00")
        )


def test_plan_update_failure_when_amount_negative(setup_test_db):
   
    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00"))
    
    with pytest.raises(ValueError):
        repo.update(
            plan_id=plan.plan_id,
            plan_name="plan 01",
            amount=Decimal("-10.00")
        )
    
# ------ DELETE PLAN TESTS ------

def test_delete_plan_success(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )
    
    result = repo.delete(plan.plan_id)

    assert result is True

    deleted = repo.get(plan.plan_id)

    assert deleted is None

def test_delete_plan_not_found(setup_test_db):

    repo = SQLitePlanRepository()

    result = repo.delete(plan_id=uuid4())

    assert result is False

def test_delete_plan_twice(setup_test_db):

    repo = SQLitePlanRepository()

    plan = repo.create(plan_name="plan 01",
                       period_days=30,
                       amount=Decimal("10.00")
                       )

    assert repo.delete(plan.plan_id) is True
    assert repo.delete(plan.plan_id) is False

