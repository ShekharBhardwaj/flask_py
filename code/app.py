from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'Shekhar'
api = Api(app)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity) #/auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'item {name} already exists'}, 400
        payload = Item.parser.parse_args()
        item = {'name': name, 'price': payload['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        payload = Item.parser.parse_args()
        if item is None:
            item = {"name": name, "price": payload["price"]}
            items.append(item)
        else:
            item.update(payload)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/user/register')

app.run(port=5000, debug=True)