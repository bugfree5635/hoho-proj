from fastapi.testclient import TestClient
from datetime import datetime, timezone
from jose import jwt
from app.main import app
from app.security.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.security.auth import (
    ALGORITHM,
    SECRET_KEY,
)

client = TestClient(app)


def test_hash_password():
    password = "123456"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    assert response.status_code == 200


def test_create_access_token():
    data = {"sub": "henry"}

    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert decoded["sub"] == "henry"
    assert "exp" in decoded
    assert "exp" not in data

    # Make sure the expiration is in the future
    assert decoded["exp"] > datetime.now(timezone.utc).timestamp()


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "henry",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
