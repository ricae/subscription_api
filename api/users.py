from flask_restx import Resource, reqparse
from models import db, UserModel

class Users(Resource):

    def get(self, user_id=None):

        # fetching single user
        if user_id:
            user = UserModel.query.get(user_id)
            if user:
                return user.to_dict()
            
            return {"error": "user not found"}, 404
        
        # fetching all users
        users = UserModel.query.all()
        return [user.to_dict() for user in users]
    
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument("phone", type=str, required=False)
        parser.add_argument("email", type=str, required=False)
        parser.add_argument("username", type=str, required=False)
        args = parser.parse_args()

        # only one required
        phone = args["phone"]
        email = args["email"]
        username = args["username"]

        if phone==None and email==None and username==None:
            return {"error": "please input phone/email/username"}, 400

        # avoid duplicate user
        users = UserModel.query.all()
        for user in users:
            if phone:
                if phone == user.phone:
                    return {"error": "user already exists"}, 400
            if email:
                if email == user.email:
                    return {"error": "user already exists"}, 400
            if username:
                if username == user.username:
                    return {"error": "user already exists"}, 400

        new_user = UserModel(phone=phone, email=email, username=username)
        db.session.add(new_user)
        db.session.commit()
        return {"msg": "successfully added new user"}, 201

    def delete(self, user_id):
        
        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'msg': 'user deleted'}, 200
        
        return {"error": "user not found"}, 404
    