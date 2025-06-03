import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_eduid():
    response = client.post("/eduid/create", json={"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_eduid():
    response = client.get("/eduid/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_update_eduid():
    response = client.put("/eduid/1", json={"name": "John Smith"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Smith"

def test_delete_eduid():
    response = client.delete("/eduid/1")
    assert response.status_code == 204

def test_get_nonexistent_eduid():
    response = client.get("/eduid/999")
    assert response.status_code == 404