import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


@app.route('/drinks')
def get_drinks():
    """ Get all drinks. Public endpoint """
    try:
        # Get all the drinks from the database
        drinks = Drink.query.all()

        # Return a status code 200 and json of drinks list and set the success message to true
        return jsonify({
            'success': True,
            'drinks': [d.short() for d in drinks]
        }), 200
    except:
        abort(500)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    """ Get drink details. Need get:drinks-detail permission """
    try:
        # Get all the drinks from the database
        drinks = Drink.query.all()

        # Return a status code 200 and json of drinks list and set the success message to true
        return jsonify({
            'success': True,
            'drinks': [d.long() for d in drinks]
        }), 200
    except:
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    """ Post request to add a drink. Needs post:drinks permission """
    body = request.get_json()       # Read post data
    # Check if required fields exist
    if 'title' not in body or 'recipe' not in body:
        abort(422)

    title = body['title']
    recipe = body['recipe']

    # recipe is a list of dict
    # [{'color': string, 'name':string, 'parts':number}]
    if not isinstance(recipe, list):
        abort(422)

    # Checking if all the required ingredient fields present
    for ingredient in recipe:
        if 'color' not in ingredient or 'name' not in ingredient or 'parts' not in ingredient:
            abort(422)

    # Converting to a lazy json blob
    recipe = json.dumps(recipe)

    try:
        # Create an instance of the Drink model
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        }), 200
    except:
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    """ Update a drink. Needs patch:drinks permission """
    # Retrieve the specified drink from the database by its ID
    drink = Drink.query.get(id)
    # Check if the drink exists in the database
    if drink is None:
        abort(404)

    body = request.get_json()
    if 'title' not in body and 'recipe' not in body:
        abort(422)

    title = body.get('title')
    recipe = body.get('recipe')

    if title is not None:
        drink.title = title

    if recipe is not None:
        # recipe is a list of dict
        # [{'color': string, 'name':string, 'parts':number}]
        if not isinstance(recipe, list):
            abort(422)

        # Checking if all the required ingredient fields present
        for ingredient in recipe:
            if 'color' not in ingredient or 'name' not in ingredient or 'parts' not in ingredient:
                abort(422)

        # Converting to a lazy json blob
        recipe = json.dumps(recipe)
        drink.recipe = recipe

    try:
        # Update the drink data
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    """ Delete a drink. Needs delete:drinks permission """
    drink = Drink.query.get(id)
    # Check if the drink exists in the database
    if not drink:
        abort(404)

    try:
        # Delete the drink from the database
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)


#  ####### Error Handling #########


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Not Processable'
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405


@app.errorhandler(AuthError)
def auth_error(e):
    """ AuthError exception """
    return jsonify({
        'success': False,
        'error': e.status_code,
        'message': e.error['description']
    }), e.status_code
