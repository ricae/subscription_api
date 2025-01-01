import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestProducts:

    def test_successful_fetching_products(self, client):
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        assert response.json == [
            {
                "id": 1,
                "name": "first product",
            }
        ]

    def test_successful_fetching_a_product(self, client):
        response = client.get("/api/v1/products/1")
        assert response.status_code == 200
        assert response.json == {
                "id": 1,
                "name": "first product",
            }
        
    def test_failed_fetching_a_product(self, client):
        response = client.get("/api/v1/products/99")
        assert response.status_code == 404
        assert response.json["error"] == "product not found"
        
    def test_failed_adding_product(self, client):
        response = client.post(
            "api/v1/products",
            data = {
                "name": "first product",
            }
        )
        assert response.status_code == 400
        assert response.json["error"] == "product already exists"

    

    