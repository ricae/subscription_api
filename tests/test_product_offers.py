import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestProductOffers:
    
    def test_successful_adding_product(self, client):
        response = client.post(
            "api/v1/products",
            data = {
                "name": "first product",
            }
        )
        assert response.status_code == 201
        assert response.json["msg"] == "successfully added new product"

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

    def test_failed_adding_offer_duplicate(self, client):
        response = client.post(
            "api/v1/offers",
            data = {
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "monthly"
            }
        )
        assert response.status_code == 400
        assert response.json["error"] == "offer already exists"

    def test_failed_adding_offer_productnotfound(self, client):
        response = client.post(
            "api/v1/offers",
            data = {
                "product_id": 99,
                "price": 149,
                "subscription_frequency": "monthly"
            }
        )
        assert response.status_code == 404
        assert response.json["error"] == "product not found"

    def test_failed_adding_offer_invalidsubfreq(self, client):
        response = client.post(
            "api/v1/offers",
            data = {
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "yearly"
            }
        )
        assert response.status_code == 400
        assert response.json["error"] == "invalid subscription frequency"

    def test_successful_getting_offers(self, client):
        response = client.get("api/v1/offers")
        assert response.status_code == 200
        assert response.json == [
            {
                "id": 1,
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "monthly"
            }
        ]

    def test_successful_getting_an_offer(self, client):
        response = client.get("api/v1/offers/1")
        assert response.status_code == 200
        assert response.json == {
                "id": 1,
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "monthly"
            }
    
    def test_failed_getting_an_offer(self, client):
        response = client.get("api/v1/offers/99")
        assert response.status_code == 404
        assert response.json["error"] == "offer not found"
        
    def test_successful_getting_offers_of_product(self, client):
        response = client.get("api/v1/products/1/offers")
        assert response.status_code == 200
        assert response.json == [
            {
                "id": 1,
                "product_id": 1,
                "price": 149,
                "subscription_frequency": "monthly"
            }
        ]

    def test_successful_deleting_offer(self, client):
        response = client.delete("api/v1/offers/1")
        assert response.status_code == 200
        assert response.json["msg"] == "successfully deleted offer"

    def test_failed_deleting_offer(self, client):
        response = client.delete("api/v1/offers/1")
        assert response.status_code == 404
        assert response.json["error"] == "offer not found"