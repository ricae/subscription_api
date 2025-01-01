from flask_restx import Resource, reqparse
from models import db, ProductModel, ProductOfferModel


class ProductOffers(Resource):

    def get(self, product_id=None, offer_id=None):

        offers = ProductOfferModel.query.all()

        # fetching offers of specific product
        if product_id:
            product = ProductModel.query.get(product_id)
            if not product:
                return {"error": "product not found"}, 404  
            
            return [offer.to_dict() for offer in offers if offer.product_id == product_id]

        # fetching specific offer
        if offer_id:
            offer = ProductOfferModel.query.get(offer_id)
            if not offer:
                return {"error": "offer not found"}, 404  
            
            return offer.to_dict()
        
        # fetching all offers
        return [offer.to_dict() for offer in offers]

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, required=True)
        parser.add_argument("price", type=float, required=True)
        parser.add_argument("subscription_frequency", type=str, required=True)
        args = parser.parse_args()

        product_id = args["product_id"]
        price = args["price"]
        subscription_frequency = args["subscription_frequency"]

        # check if product exists
        product = ProductModel.query.get(product_id)
        if not product:
            return {"error": "product not found"}, 404  

        # check valid subscription frequency
        if subscription_frequency.upper() not in ProductOfferModel.SUBSCRIPTION_FREQUENCY_CHOICES:
            return {"error": "invalid subscription frequency"}, 400

        # avoid duplicate offer
        offers = ProductOfferModel.query.all()
        for offer in offers:
            if product_id == offer.product_id and price == offer.price and subscription_frequency == offer.subscription_frequency:
                return {"error": "offer already exists"}, 400

        new_offer = ProductOfferModel(product_id=product_id, price=price, subscription_frequency=subscription_frequency)
        db.session.add(new_offer)
        db.session.commit()
        return {"msg": "successfully added new offer"}, 201

    def delete(self, offer_id):

        offer = ProductOfferModel.query.get(offer_id)
        if not offer:
            return {"error": "offer not found"}, 404
        
        db.session.delete(offer)
        db.session.commit()
        return {"msg": "successfully deleted offer"}, 200