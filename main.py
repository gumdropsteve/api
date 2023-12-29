import pandas as pd
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

visits_path = './data/osmosis_visits_world.csv'
avg_visit_path = './data/osmosis_average_visit_duration_world.csv'
telegram_path = './telegram_data'


class status (Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


class Both(Resource):

    def get(self, todo_id):
        """
        return number of visitors and average visit duration 
        for a given token's website
        """

        if todo_id == 'osmosis':
            data = pd.read_csv(visits_path)
            df = pd.read_csv(avg_visit_path)['average_visit_duration']
            data = pd.concat([data, df], axis=1)
        else:
            # clean up the endpoint if necessary
            if (todo_id == 'sushiswap') or (todo_id == 's'):
                todo_id = 'sushi'
            elif (todo_id == 'joe') or (todo_id == 'traderjoe'):
                todo_id = 'traderjoexyz'
            # call the specific token requested
            data = pd.read_csv(visits_path.replace('osmosis', todo_id))
            df = pd.read_csv(avg_visit_path.replace('osmosis', todo_id))['average_visit_duration']
            data = pd.concat([data, df], axis=1)
            
        data = data.to_dict()
        return {'data': data}, 200
    

class Telegram(Resource):

    def get(self, todo_id):
        """
        return raw telegram data 
        for a given token's official telegram
        """
        # call the specific token requested
        data = pd.read_csv(f'{telegram_path}/{todo_id}_telegram_raw.csv')
            
        data = data.to_dict()
        return {'data': data}, 200
    

# class Chart(Resource):

#     def get(self, todo_id):

#         if todo_id == 'osmosis':
#             data = pd.read_csv(visits_path)
#             df = pd.read_csv(avg_visit_path)['average_visit_duration']
#             data = pd.concat([data, df], axis=1)
#         else:
#             # clean up the endpoint if necessary
#             if (todo_id == 'sushiswap') or (todo_id == 's'):
#               todo_id = 'sushi'
#             # call the specific token requested
#             data = pd.read_csv(visits_path.replace('osmosis', todo_id))
#             df = pd.read_csv(avg_visit_path.replace('osmosis', todo_id))['average_visit_duration']
#             data = pd.concat([data, df], axis=1)
            
#         data = data.plot.bar('date', 'visits')
#         return {'data': data}, 200


# add api endpoints
api.add_resource(status, '/')
api.add_resource(Both, '/<string:todo_id>')
api.add_resource(Telegram, '/telegram/<string:todo_id>')
# api.add_resource(Chart, '/chart/<string:todo_id>')

if __name__ == '__main__':
    app.run()
