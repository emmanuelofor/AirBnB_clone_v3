#!/usr/bin/python3
'''
    This script sets up Flask application, registers the blueprint and initializes CORS.
'''
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")  # Initialize Cross Origin Resource Sharing (CORS)
app.register_blueprint(app_views)  # Register the blueprint to the application


@app.teardown_appcontext
def tear_down(self):
    '''
    Close the current SQLAlchemy Session after each request.
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
    Handle 404 errors by returning a JSON formatted response.
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Run the Flask application using the host and port specified in the environment variables
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
