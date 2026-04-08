import pytest
from uuid import UUID, uuid4
from billing.repos.customer_repository import SQLiteCustomerRepository


# ------ CREATE CUSTOMER TESTS ------

def test_create_customer_success(setup_test_db):

    repo = SQLiteCustomerRepository()

    customer = repo.create(
        email = "test@example.com",
        first_name = "Jane",
        last_name = "Doe"
    )

    assert customer.email == "test@example.com"
    assert customer.first_name == "Jane"
    assert customer.last_name == "Doe"
    assert isinstance(customer.customer_id, UUID)

def test_create_customer_raises_error_when_email_missing(setup_test_db):

    repo = SQLiteCustomerRepository()

    with pytest.raises(ValueError):
        repo.create(email="")

# ------ GET CUSTOMER TESTS ------

def test_get_customer_by_id_success(setup_test_db):

    repo = SQLiteCustomerRepository()

    customer = repo.create(
        email = "test@example.com"
    )

    result = repo.get(customer.customer_id)

    assert result is not None
    assert result.customer_id == customer.customer_id
    assert result.email == "test@example.com"

def test_get_customer_by_id_failure(setup_test_db):

    repo = SQLiteCustomerRepository()

    repo.create(email = "test@example.com")

    fake_id = uuid4()

    result = repo.get(fake_id)

    assert result is None

def test_get_customer_invalid_id_type(setup_test_db):

    repo = SQLiteCustomerRepository()

    repo.create(email = "test@example.com")

    result = repo.get("not-a-uuid")

    assert result is None

# ------ GET CUSTOMER LISTS TESTS -------

def test_get_customers_list_returns_list(setup_test_db):

    repo = SQLiteCustomerRepository()

    repo.create(email="user_1@email.com")
    repo.create(email="user_2@email.com")

    result = repo.list()
    emails = [c.email for c in result]

    assert len(result) == 2
    assert set(emails) == {"user_1@email.com", "user_2@email.com"}

def test_get_customers_list_returns_empty_list(setup_test_db):

    repo = SQLiteCustomerRepository()

    result = repo.list()

    assert result == []

# ------ PATCH/UPDATE CUSTOMERS TESTS ------

def test_update_customer_success(setup_test_db):
    
    repo = SQLiteCustomerRepository()

    customer = repo.create(
        email="name@example.com",
        first_name="Jane",
        last_name="Doe"
        )
    
    repo.update(
        customer_id=customer.customer_id,
        email="new@example.com"
    )

    updated = repo.get(customer.customer_id)

    assert updated is not None
    assert updated.email == "new@example.com"
    assert updated.first_name == "Jane"
    assert updated.last_name == "Doe"

def test_update_customer_failure_with_invalid_id(setup_test_db):

    repo = SQLiteCustomerRepository()

    customer = repo.create(email="test@example.com")

    result = repo.update(
        customer_id=uuid4(),
        email="new@example.com"
    )

    assert result is None

    existing = repo.get(customer.customer_id)

    assert existing is not None
    assert existing.email == "test@example.com"

# ------ DELETE CUSTOMER TESTS ------

def test_delete_customer_success(setup_test_db):
    repo = SQLiteCustomerRepository()

    customer = repo.create(email="test@example.com")

    result = repo.delete(customer.customer_id)

    assert result is True

    deleted = repo.get(customer.customer_id)
    assert deleted is None

def test_delete_customer_not_found(setup_test_db):
    repo = SQLiteCustomerRepository()

    result = repo.delete(
        customer_id=uuid4()
    )

    assert result is False

def test_delete_customer_twice(setup_test_db):
    repo = SQLiteCustomerRepository()

    customer = repo.create(email="test@example.com")

    assert repo.delete(customer.customer_id) is True
    assert repo.delete(customer.customer_id) is False

