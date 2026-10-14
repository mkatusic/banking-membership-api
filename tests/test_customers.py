from uuid import uuid4


def test_create_customer(client):
    email = f"test-{uuid4().hex}@example.com"

    response = client.post(
        "/customers",
        json={
            "name": "Test Customer",
            "email": email,
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["name"] == "Test Customer"
    assert response_data["email"] == email
    assert "id" in response_data