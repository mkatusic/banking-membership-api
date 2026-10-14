from app.services.idempotency_service import generate_request_hash


def test_same_request_produces_same_hash():
    request_a = {
        "customer_id": 5,
        "plan_id": 4,
    }

    request_b = {
        "plan_id": 4,
        "customer_id": 5,
    }

    hash_a = generate_request_hash(request_a)
    hash_b = generate_request_hash(request_b)

    assert hash_a == hash_b

def test_different_requests_produce_different_hashes():
    request_a = {
        "customer_id": 5,
        "plan_id": 4,
    }

    request_b = {
        "customer_id": 5,
        "plan_id": 2,
    }

    assert generate_request_hash(request_a) != generate_request_hash(request_b)
    