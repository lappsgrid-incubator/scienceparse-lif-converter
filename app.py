"""app.py

Run the converter as a RESTful Flask application.

Usage:

$ python3 app.py

This gives access to two URLs:

$ curl 127.0.0.1:5000
$ curl -X POST -d@data/input.json 127.0.0.1:5000/parse

The first returns some metadata and the second a LIF string created from the
input file.

"""


import json

from flask import Flask, request, Response

from converter import Converter


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    obj = { "application": "sienceparse2lif",
            "description": "Takes ScienceParse output and converts it into LIF." }
    return json.dumps(obj, indent=4) + '\n'


@app.route('/parse', methods=['POST'])
def parse():
    data = json.loads(request.get_data())
    container = Converter(json.dumps(data))
    return Response(response=container.as_json_string(),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':

    app.run(debug=True)

    
