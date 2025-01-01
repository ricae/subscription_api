import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestSubscriptions:

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
     
    def test_successful_adding_offer(self, client):
        response = client.post(
            "api/v1/offers",
            data = {
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "monthly"
            }
        )
        assert response.status_code == 201
        assert response.json["msg"] == "successfully added new offer"

    def test_successful_fetching_subscriptions(self, client):
        response = client.get("/api/v1/subscriptions")
        assert response.status_code == 200
        assert response.json == {
            
                "subscribed": [],
                "unsubscribed": []
            
        }

    def test_successful_adding_subscription(self, client):
        response = client.post(
            "api/v1/subscriptions",
            data = {
                "linked_account": 1,
                "subscribed_product": 1,
                "product_offer": 1, 
            }
        )
        assert response.status_code == 201
        assert response.json["msg"] == "successfully added new subscription"

    def test_failed_adding_subscription(self, client):
        response = client.post(
            "api/v1/subscriptions",
            data = {
                "linked_account": 1,
                "subscribed_product": 1,
                "product_offer": 1, 
            }
        )
        assert response.status_code == 400
        assert response.json["error"] == "subscription already exists"

    def test_failed_adding_subscription_usernotfound(self, client):
        response = client.post(
            "api/v1/subscriptions",
            data = {
                "linked_account": 2,
                "subscribed_product": 1,
                "product_offer": 1, 
            }
        )
        assert response.status_code == 404
        assert response.json["error"] == "user not found"

    def test_failed_adding_subscription_productnotfound(self, client):
        response = client.post(
            "api/v1/subscriptions",
            data = {
                "linked_account": 1,
                "subscribed_product": 2,
                "product_offer": 1, 
            }
        )
        assert response.status_code == 404
        assert response.json["error"] == "product not found"

    def test_failed_adding_subscription_offernotfound(self, client):
        response = client.post(
            "api/v1/subscriptions",
            data = {
                "linked_account": 1,
                "subscribed_product": 1,
                "product_offer": 2, 
            }
        )
        assert response.status_code == 404
        assert response.json["error"] == "product offer not found"

    def test_failed_updating_subscription_stillactive(self, client):
        response = client.put("api/v1/subscriptions/1")
        assert response.status_code == 400
        assert response.json == {"error": "subscription still active"}

    def test_failed_updating_subscription_notfound(self, client):
        response = client.put("api/v1/subscriptions/99")
        assert response.status_code == 404
        assert response.json == {"error": "subscription not found"}

    def test_successful_deleting_subscription(self, client):
        response = client.delete("api/v1/subscriptions/1")
        assert response.status_code == 200
        assert response.json == {'msg': 'successfully unsubscribed'}

    def test_failed_deleting_subscription(self, client):
        response = client.delete("api/v1/subscriptions/1")
        assert response.status_code == 400
        assert response.json == {'error': 'subscription not active'}

    def test_successful_updating_subscription(self, client):
        response = client.put("api/v1/subscriptions/1")
        assert response.status_code == 201
        assert response.json == {"msg": "subscription updated"}

    def test_successful_deleting_a_user(self, client):
        response = client.delete("api/v1/users/1")
        assert response.status_code == 200
        assert response.json == {'msg': 'user deleted'}