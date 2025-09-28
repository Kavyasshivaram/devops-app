import pytest
from app.app import app  # Import the Flask app instance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, DevOps Pipeline!" in response.data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}

def test_metrics(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b"devops_app_requests_total" in response.data
