from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message': f'Item {name} not found'}, 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': f'item {name} already exists'}, 400
        payload = Item.parser.parse_args()
        item = ItemModel(name, payload['price'], payload['store_id'])
        try:
            item.save_to_db()
        except Exception as e:
            return {"message": f"Error occurred inserting the item, {e}"}
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": f"Item {name} deleted from db"}, 201
        return {"message": f"No such item {name} found"}, 404

    def put(self, name):
        payload = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item is None:
            item = ItemModel(name, payload["price"], payload['store_id'])
        else:
            item.price = payload['price']
            item.store_is = payload['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}