from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


db = SQLAlchemy()

class ProductModel(db.Model):
    __tablename__ = 'product_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "name": self.name}
    
class ProductOfferModel(db.Model):
    __tablename__ = 'offer_table'
    
    SUBSCRIPTION_FREQUENCY_CHOICES = ["DAILY", "WEEKLY", "MONTHLY"]

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_table.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    subscription_frequency = db.Column(db.String(7), nullable=False)

    def to_dict(self):
        return {"id": self.id, 
                "product_id": self.product_id, 
                "price": self.price, 
                "subscription_frequency": self.subscription_frequency}
    
class UserModel(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {"id": self.id, 
                "phone": self.phone, 
                "email": self.email,
                "username": self.username}
    
class SubscriptionModel(db.Model):
    __tablename__ = 'subscription_table'

    id = db.Column(db.Integer, primary_key=True)
    linked_account = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    subscribed_product = db.Column(db.Integer, db.ForeignKey('product_table.id'), nullable=False)
    product_offer = db.Column(db.Integer, db.ForeignKey('offer_table.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    renewed_date = db.Column(db.DateTime, default=None)
    end_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {"id": self.id, 
                "linked_account": self.linked_account,
                "subscribed_product": self.subscribed_product,
                "product_offer": self.product_offer, 
                "start_date": self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                "renewed_date": self.renewed_date.strftime('%Y-%m-%d %H:%M:%S') if self.renewed_date is not None else None,
                "end_date": self.end_date.strftime('%Y-%m-%d %H:%M:%S')
                }
    
    def get_end_date(starting_day, product_offer):
        
        if product_offer.subscription_frequency.upper() == 'DAILY':
            end_date = starting_day + timedelta(days=1)
        elif product_offer.subscription_frequency.upper() == 'WEEKLY':
            end_date = starting_day + timedelta(days=7)
        elif product_offer.subscription_frequency.upper() == 'MONTHLY':
            end_date = starting_day + timedelta(days=30)

        return end_date
