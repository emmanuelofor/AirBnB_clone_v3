#!/usr/bin/python3
'''
    Flask application with general routes:
        /status:    returns "status":"OK"
        /stats:     returns total count of all classes
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    '''
        Returns a JSON object indicating a successful status
    '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def storage_counts():
    '''
        Retrieves and returns counts of all class instances in storage
    '''
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
