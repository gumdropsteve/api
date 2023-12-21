from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

# /users
visits_path = './data/osmosis_visits_world.csv'
# /locations
avg_visit_path = './data/osmosis_average_visit_duration_world.csv'


class Visitors(Resource):

    def get(self, todo_id):
        if todo_id == 'osmosis':
            data = pd.read_csv(visits_path)
        else:
            if todo_id == 'sushiswap':
                todo_id = 'sushi'
            data = pd.read_csv(visits_path.replace('osmosis', todo_id))
        
        data = data.to_dict()
        return {'data': data}, 200


class SessionDuration(Resource):

    def get(self, todo_id):
        if todo_id == 'osmosis':
            data = pd.read_csv(avg_visit_path)
        else:
            # clean up the endpoint if necessary
            if (todo_id == 'sushiswap') or (todo_id == 's'):
                todo_id = 'sushi'
            # call the specific token requested
            data = pd.read_csv(avg_visit_path.replace('osmosis', todo_id))
        
        data = data.to_dict()
        return {'data': data}, 200


class Both(Resource):

    def get(self, todo_id):
        if todo_id == 'osmosis':
            data = pd.read_csv(visits_path)
            df = pd.read_csv(avg_visit_path)['average_visit_duration']
            data = pd.concat([data, df], axis=1)
        else:
            # clean up the endpoint if necessary
            if (todo_id == 'sushiswap') or (todo_id == 's'):
                todo_id = 'sushi'
            # call the specific token requested
            data = pd.read_csv(visits_path.replace('osmosis', todo_id))
            df = pd.read_csv(avg_visit_path.replace('osmosis', todo_id))['average_visit_duration']
            data = pd.concat([data, df], axis=1)
        
        data = data.to_dict()
        return {'data': data}, 200


# add api endpoints
api.add_resource(Visitors, '/visits/<string:todo_id>')
api.add_resource(SessionDuration, '/avg_visit/<string:todo_id>')
api.add_resource(Both, '/<string:todo_id>')

# run the api
if __name__ == "__main__":
    app.run()

