"""
File:           app.py
Created on:     01/01/2021, 19:01
"""
import datetime
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import Movies, Actors, db
from auth import AuthError, requires_auth

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    """ GET api to get all movies from the db """
    # Convert to json data
    movies = [movie.format() for movie in Movies.query.all()]
    return jsonify({
        'success': True,
        'movies': movies
    }), 200


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(payload):
    """ POST api to create a new movie in the db"""
    body = request.get_json()  # Read post data
    title = body.get('title')
    release_date = body.get('release_date')     # Should be in iso format
    if title is None or release_date is None:
        abort(400)

    try:
        # Convert release date to python date object
        release_date = datetime.datetime.fromisoformat(release_date)
        # Create a movie
        movie = Movies(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'created': movie.id
        }), 201
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movies(payload,movie_id):
    """ PATCH api to update a movie """
    # Retrieve the specified movie from the database by its ID
    movie = Movies.query.get(movie_id)
    # Check if the movie exists in the database
    if movie is None:
        abort(404)

    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')

    if title is not None:
        movie.title = title

    if release_date is not None:
        # Convert release date to python date object
        release_date = datetime.datetime.fromisoformat(release_date)
        movie.release_date = release_date

    try:
        # Update the movie data
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, movie_id):
    """ DELETE api to delete a movie from db """
    # Retrieve the specified movie from the database by its ID
    movie = Movies.query.get(movie_id)
    # Check if the movie exists in the database
    if movie is None:
        abort(404)

    try:
        # Delete the movie from the db
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie.id
        }), 200
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/actors', methods=['GET'])
@requires_auth('get:actor')
def get_actors(payload):
    """ GET api to get all actors from db """
    # Convert to json data
    actors = [actor.format() for actor in Actors.query.all()]
    return jsonify({
        'success': True,
        'actors': actors
    }), 200


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors(payload):
    """ POST api to create a new actor in db """
    body = request.get_json()  # Read post data
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if name is None or age is None or gender is None:
        abort(400)

    # Convert age to int
    age = int(age)
    try:
        # Create an actor
        actor = Actors(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'created': actor.id
        }), 201
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actors(payload, actor_id):
    """ PATCH api to update a actor """
    # Retrieve the specified actor from the database by its ID
    actor = Actors.query.get(actor_id)
    # Check if the actor exists in the database
    if actor is None:
        abort(404)

    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if name is not None:
        actor.name = name

    if age is not None:
        actor.age = int(age)

    if gender is not None:
        actor.gender = gender

    try:
        # Update the actor data
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route("/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, actor_id):
    """ DELETE api to delete a actor from db """
    # Retrieve the specified actor from the database by its ID
    actor = Actors.query.get(actor_id)
    # Check if the actor exists in the database
    if actor is None:
        abort(404)

    try:
        # Delete the movie from the db
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor.id
        }), 200
    except Exception as err:
        print(err)
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


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


if __name__ == '__main__':
    app.run()
