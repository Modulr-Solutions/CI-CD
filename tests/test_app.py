import pytest
import sys
import os

# Ajouter le dossier app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from app import app, add, subtract

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """GET / retourne status ok"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["app"] == "demo-app"

def test_health(client):
    """GET /health retourne healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_hello(client):
    """GET /hello/<name> retourne un message"""
    response = client.get("/hello/Alice")
    assert response.status_code == 200
    assert "Alice" in response.get_json()["message"]

def test_hello_autre_nom(client):
    """GET /hello/<name> fonctionne avec n'importe quel nom"""
    response = client.get("/hello/Bob")
    assert response.status_code == 200
    assert "Bob" in response.get_json()["message"]

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5