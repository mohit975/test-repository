from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        # return {}
        if store:
            return store.json()
        return {'message':'no store'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'exists'} ,400
        store = StoreModel(name)
        try:
            store.save_to_db()
            # return {'message':'Store created'} ,200
        except Exception as e:
            return {'message':'An error occured'}, 500

        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleated'}

class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
