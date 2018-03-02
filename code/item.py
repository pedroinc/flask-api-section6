import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(Item.database_file)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1] } }, 200

    # @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #bad req status code

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        connection = sqlite3.connect(Item.database_file)
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    # @jwt_required()
    def delete(self, name):
        if not self.find_by_name(name):
            return {'message': "Item not found"}, 404 #not found

        connection = sqlite3.connect(Item.database_file)
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    #create or update existing items
    # @jwt_required()
    def put(self, name):
        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price'] }
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(Item.database_file)
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()

        items = []
        for row in rows:
            items.append({'item': {'name': row[0], 'price': row[1] } })

        return {'items': items}, 200
