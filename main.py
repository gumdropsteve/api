import pandas as pd
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

visits_path = './data/osmosis_visits_world.csv'
avg_visit_path = './data/osmosis_average_visit_duration_world.csv'


class status (Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


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
api.add_resource(status, '/')
api.add_resource(Both, '/<string:todo_id>')

if __name__ == '__main__':
    app.run()
