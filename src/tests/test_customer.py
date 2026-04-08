from datetime import datetime, timezone
from uuid import UUID, uuid4
from billing.domain.customer import Customer

# ------ UUID ------

def test_customer_stores_provided_uuid_id():
    provided_id = uuid4()

    customer = Customer(
        email= "example@email.com",
        customer_id=provided_id
    )

    assert customer.customer_id == provided_id
    assert isinstance(customer.customer_id, UUID)

def test_customer_generates_unique_UUID_id_when_not_provided():
    customer1 = Customer(
        email= "example1@email.com",
    )
    customer2 = Customer(
        email="example2@email.com",
    )

    assert customer1.customer_id is not None
    assert customer2.customer_id is not None
    assert customer1.customer_id != customer2.customer_id
    assert isinstance(customer1.customer_id, UUID)
    
# ------- TIMESTAMP TESTS ------
def test_created_at_defaults_correctly():
    customer = Customer(
        email= "example@email.com",
    )

    assert customer.created_at is not None
    assert customer.created_at.tzinfo is not None


