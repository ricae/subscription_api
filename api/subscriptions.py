from flask_restx import Resource, reqparse
from models import db, SubscriptionModel, UserModel, ProductModel, ProductOfferModel
from datetime import datetime, timedelta


class Subscriptions(Resource):

    def get(self, user_id=None, product_id=None, subscription_id=None):

        subscriptions = SubscriptionModel.query.all()
        states = {"subscribed": [], "unsubscribed": []}

        # fetching subscriptions of specific user
        if user_id:
            
            user = UserModel.query.get(user_id)
            if not user:
                return {"error": "user not found"}, 404
            
            for subscription in subscriptions:
                if subscription.linked_account == user_id:
                    if subscription.end_date > datetime.now():
                        states["subscribed"].append(subscription.to_dict())
                    else:
                        states["unsubscribed"].append(subscription.to_dict())
            return states
        
        # fetching subscriptions of specific product
        if product_id:
            
            product = ProductModel.query.get(product_id)
            if not product:
                return {"error": "product not found"}, 404
            
            for subscription in subscriptions:
                if subscription.subscribed_product == product_id:
                    if subscription.end_date > datetime.now():
                        states["subscribed"].append(subscription.to_dict())
                    else:
                        states["unsubscribed"].append(subscription.to_dict())
            return states

        # fetching a subscription
        if subscription_id:
            subscription = SubscriptionModel.query.get(subscription_id)
            if not subscription:
                return {"error": "subscription not found"}, 404
            
            return subscription.to_dict()

        # fetching all subscriptions 
        for subscription in subscriptions:
            if subscription.end_date > datetime.now():
                states["subscribed"].append(subscription.to_dict())
            else:
                states["unsubscribed"].append(subscription.to_dict())

        return states
    
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument("linked_account", type=int, required=True)
        parser.add_argument("subscribed_product", type=int, required=True)
        parser.add_argument("product_offer", type=int, required=True)
        args = parser.parse_args()

        linked_account_id = args["linked_account"]
        subscribed_product_id = args["subscribed_product"]
        product_offer_id = args["product_offer"]

        linked_account = UserModel.query.get(linked_account_id)
        if not linked_account:
            return {"error": "user not found"}, 404
        
        subscribed_product = ProductModel.query.get(subscribed_product_id)
        if not subscribed_product:
            return {"error": "product not found"}, 404
        
        product_offer = ProductOfferModel.query.get(product_offer_id)
        if not product_offer:
            return {"error": "product offer not found"}, 404
        if product_offer.product_id != subscribed_product_id:
            return {"error": "product offer not found"}, 404


        # avoid duplicate subscription
        subcriptions = SubscriptionModel.query.all()
        for sub in subcriptions:
            if linked_account_id==sub.linked_account and subscribed_product_id==sub.subscribed_product and product_offer_id==sub.product_offer:
                return {"error": "subscription already exists"}, 400
            if linked_account_id==sub.linked_account and subscribed_product_id==sub.subscribed_product and sub.end_date > datetime.now():
                return {"error": "user still has active subscription"}, 400

        start_date = datetime.now()
        end_date = SubscriptionModel.get_end_date(start_date, product_offer)
       
        new_subscription = SubscriptionModel(linked_account=linked_account_id, 
                                             subscribed_product=subscribed_product_id, 
                                             product_offer=product_offer_id,
                                             start_date=start_date, 
                                             end_date=end_date)
        db.session.add(new_subscription)
        db.session.commit()
        return {"msg": "successfully added new subscription"}, 201

    def put(self, subscription_id):

        subscription = SubscriptionModel.query.get(subscription_id)

        if not subscription:
            return {"error": "subscription not found"}, 404
        
        if subscription.end_date > datetime.now():
            return {"error": "subscription still active"}, 400
        
        subcriptions = SubscriptionModel.query.all()
        for sub in subcriptions:
            if subscription.linked_account==sub.linked_account and subscription.subscribed_product==sub.subscribed_product and sub.end_date > datetime.now():
                return {"error": "user still has active subscription"}, 400


        subscription.renewed_date = datetime.now()
        product_offer = ProductOfferModel.query.get(subscription.product_offer)
        subscription.end_date = SubscriptionModel.get_end_date(subscription.renewed_date, product_offer)
          
        db.session.commit()
        return {"msg": "subscription updated"}, 201
        
    def delete(self, subscription_id):
        
        subscription = SubscriptionModel.query.get(subscription_id)
        if not subscription:
            return {"error": "subscription not found"}, 404
        
        if subscription.end_date > datetime.now():
            subscription.end_date = datetime.now()
            db.session.commit()
            return {"msg": "successfully unsubscribed"}
        else:
            return {"error": "subscription not active"}, 400

