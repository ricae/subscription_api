from api.products import Products
from api.product_offers import ProductOffers
from api.users import Users
from api.subscriptions import Subscriptions

def register(api):
    api.add_resource(Products, "/api/v1/products", 
                     "/api/v1/products/<int:product_id>")

    api.add_resource(ProductOffers, "/api/v1/offers", 
                     "/api/v1/offers/<int:offer_id>", 
                     "/api/v1/products/<int:product_id>/offers")
    
    api.add_resource(Users, "/api/v1/users", 
                     "/api/v1/users/<int:user_id>")

    api.add_resource(Subscriptions, "/api/v1/subscriptions", 
                     "/api/v1/subscriptions/<int:subscription_id>", 
                     "/api/v1/products/<int:product_id>/subscriptions",
                     "/api/v1/users/<int:user_id>/subscriptions")


