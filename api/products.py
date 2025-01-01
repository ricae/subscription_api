from flask_restx import Resource, reqparse
from models import db, ProductModel

class Products(Resource):

    def get(self, product_id=None):

        # fetching single product
        if product_id:
            product = ProductModel.query.get(product_id)
            if not product:
                return {"error": "product not found"}, 404
            
            return product.to_dict()
        
        # fetching all products
        products = ProductModel.query.all()
        return [product.to_dict() for product in products]
    
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = parser.parse_args()

        name = args["name"]
        
        # avoid duplicate product
        products = ProductModel.query.all()
        for product in products:
            if name == product.name:
                return {"error": "product already exists"}, 400

        new_product = ProductModel(name=name)
        db.session.add(new_product)
        db.session.commit()
        return {"msg": "successfully added new product"}, 201