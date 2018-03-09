import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from common.utils import Utils
from models.item import ItemModel

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

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #bad req status code

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            ItemModel.insert(item)
        except:
            return {"message": "error while inserting the item."}, 500 # internal server error

        return item, 201

    # @jwt_required()
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {'message': "Item not found"}, 404 #not found

        connection = sqlite3.connect(Utils.DATABASE_FILE)
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name): #create or update existing items
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "error occurred while inserting the item."}, 500 # internal server error
        else:
            try:
                updated_item.update()
            except:
                return {"message": "error occurred while updating the item."}, 500 # internal server error

        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(Item.database_file)
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        # rows = result.fetchall()
        items = []
        for row in result:
            items.append( {'name': row[0], 'price': row[1] })

        connection.close()

        return {'items': items}, 200
