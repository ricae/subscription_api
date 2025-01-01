import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestUsers:

    def test_successful_adding_user(self, client):
        response = client.post(
            "api/v1/users",
            data={
                "phone": "09121231234",
                "email": "random@email.com",
                "username": "random"
            }
        )
        assert response.status_code == 201
        assert response.json["msg"] == "successfully added new user"

    def test_failed_adding_user(self, client):
        response = client.post(
            "api/v1/users",
            data={
                "phone": "09121231234",
                "email": "random@email.com",
                "username": "random"
            }
        )
        assert response.status_code == 400
        assert response.json["error"] == "user already exists"

    def test_successful_fetching_users(self, client):
        response = client.get("api/v1/users")
        assert response.status_code == 200
        assert response.json == [
            {
                "id": 1,
                "phone": "09121231234",
                "email": "random@email.com",
                "username": "random"
            }
        ]

    def test_successful_fetching_a_user(self, client):
        response = client.get("api/v1/users/1")
        assert response.status_code == 200
        assert response.json == {
                "id": 1,
                "phone": "09121231234",
                "email": "random@email.com",
                "username": "random"
            }
    
    def test_failed_fetching_a_user(self, client):
        response = client.get("api/v1/users/99")
        assert response.status_code == 404
        assert response.json == {"error": "user not found"}

    def test_successful_adding_another_user(self, client):
        response = client.post(
            "api/v1/users",
            data={
                "phone": "09121234567",
                "email": "another@email.com",
                "username": "fudgeebar"
            }
        )
        assert response.status_code == 201
        assert response.json["msg"] == "successfully added new user"

    def test_successful_deleting_a_user(self, client):
        response = client.delete("api/v1/users/2")
        assert response.status_code == 200
        assert response.json == {'msg': 'user deleted'}

    def test_failed_deleting_a_user(self, client):
        response = client.delete("api/v1/users/2")
        assert response.status_code == 404
        assert response.json == {'error': 'user not found'}
        
