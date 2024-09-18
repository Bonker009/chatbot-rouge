import pytest
from fastapi.testclient import TestClient
from app.main import app   
from app.api.auth.auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt

client = TestClient(app)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
  
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token  
def test_login_creates_jwt():
   
    response = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200

   
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

   
    token = response.json()["access_token"]
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == "testuser"

def test_login_with_invalid_credentials():
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401 