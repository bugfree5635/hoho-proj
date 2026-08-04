from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)



def test_health():

    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    assert response.json() == {
        "status":"ok"
    }


def test_create_employee(client):
    response = client.post(
        "/employees",
        json={
            "name": "Henry",
            "email": "henry@test.com",
            "department": "Security"
        }
    )

    assert response.status_code == 200