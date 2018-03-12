from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from common.utils import Utils

class Item(Resource):

    database_file = 'my_database.db'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #bad req status code

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            ItemModel.save_to_db(item)
        except:
            return {"message": "error while inserting the item."}, 500 # internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            ItemModel.delete_from_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': "Item not found"}, 404 #not found

    @jwt_required()
    def put(self, name): #create or update existing items
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        # with list comprehension
        return {'items': [item.json() for item in ItemModel.query.all()]}
        
        # with lambda
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
