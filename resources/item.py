# import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from flask import Flask,json
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field cannot be left blank!"
    )

    parser.add_argument('store_id',
    type = float,
    required = True,
    help = "This field cannot be left blank!"
    )

    @jwt_required()
    def get(self,name):
        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'messge':'item not found'},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with name {} already exist.".format(name)},400
        data = Item.parser.parse_args()
        # return {}

        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured"},500

        return item.json(),201


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = connection.cursor()
        # query = "DELETE FROM items where name=?"
        # cursor.execute(query,(name,))
        # connection.commit()
        # connection.close()
        return {'message':'item deleted'}

    def put(self,name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        # type = float,
        # required = True,
        # help = "This field cannot be left blank!"
        # )
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name,data['price'])

        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
            # try:
            #     updated_item.insert()
            # except:
            #     return {'message':'An error occured1'} ,500
        else:
            item.price = data['price']
            # try:
            #     updated_item.update()
            # except:
            #     return {'message':'An error occured2'} ,500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items':ItemModel.query.all()}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = connection.cursor()
        # query = "SELECT * FROM items"
        # cur = cursor.execute(query)
        # result = []
        # for row in cur:
        #     result.append({'name':row[0],'price':row[1]})
        #
        # connection.close()
        # return {'items':result},200
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
