"""
File:           test_app.py
Created on:     01/01/2021, 19:02
"""
import unittest
from unittest import mock
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movies, Actors


class CapstoneUnitTest(unittest.TestCase):
    """ Test cases """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config["DEBUG"] = False
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_get_movies_pass(self, mock_verify_decode, mock_check_perm):
        """ Test GET request to movies pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().get('/movies', headers={'Authorization': 'Bearer abcd'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_get_movies_fail(self, mock_verify_decode, mock_check_perm):
        """ Test GET request to movies fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().get('/movies', headers={'Authorization': 'Bearer1 abcd'})
        self.assertEqual(response.status_code, 401)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_post_movies_pass(self, mock_verify_decode, mock_check_perm):
        """ Test POST request to movies pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().post(
                '/movies',
                headers={'Authorization': 'Bearer abcd'},
                json={'title': 'Dhoom', 'release_date': '2021-01-08T20:58:29.732421'}
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_post_movies_fail(self, mock_verify_decode, mock_check_perm):
        """ Test POST request to movies fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().post(
                '/movies',
                headers={'Authorization': 'Bearer abcd'},
                json={'title': 'Dhoom'}
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_patch_movies_pass(self, mock_verify_decode, mock_check_perm):
        """ Test PATCH request to movies pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            movie = Movies(
                title='Movie1',
                release_date='2021-01-08T20:58:29.732421'
            )
            self.db.session.add(movie)
            self.db.session.commit()
            response = self.client().patch(
                f'/movies/{movie.id}',
                headers={'Authorization': 'Bearer abcd'},
                json={'title': 'Movie11'}
            )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_patch_movies_fail(self, mock_verify_decode, mock_check_perm):
        """ Test PATCH request to movies fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        response = self.client().patch(
            f'/movies/1111',
            headers={'Authorization': 'Bearer abcd'},
            json={'title': 'Movie11'}
        )
        self.assertEqual(response.status_code, 404)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_detele_movies_pass(self, mock_verify_decode, mock_check_perm):
        """ Test DELETE request to movies pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            movie = Movies(
                title='Movie10',
                release_date='2021-01-08T20:58:29.732421'
            )
            self.db.session.add(movie)
            self.db.session.commit()
            response = self.client().delete(
                f'/movies/{movie.id}',
                headers={'Authorization': 'Bearer abcd'}
            )
        data = json.loads(response.data)
        expected_data = {
            'success': True,
            'deleted': movie.id
        }
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_detele_movies_fail(self, mock_verify_decode, mock_check_perm):
        """ Test DELETE request to movies pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        response = self.client().delete(
            f'/movies/1111',
            headers={'Authorization': 'Bearer abcd'}
        )
        self.assertEqual(response.status_code, 404)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_get_actors_pass(self, mock_verify_decode, mock_check_perm):
        """ Test GET request to actors pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().get('/actors', headers={'Authorization': 'Bearer abcd'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_get_actors_fail(self, mock_verify_decode, mock_check_perm):
        """ Test GET request to actors fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().get('/actors', headers={'Authorization': 'Bearer1 abcd'})
        self.assertEqual(response.status_code, 401)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_post_actors_pass(self, mock_verify_decode, mock_check_perm):
        """ Test POST request to actors pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().post(
                '/actors',
                headers={'Authorization': 'Bearer abcd'},
                json={'name': 'minu', 'age': 26, 'gender': 'female'}
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_post_actors_fail(self, mock_verify_decode, mock_check_perm):
        """ Test POST request to actors fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            response = self.client().post(
                '/actors',
                headers={'Authorization': 'Bearer abcd'},
                json={'name': 'renad'}
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_patch_actors_pass(self, mock_verify_decode, mock_check_perm):
        """ Test PATCH request to actors pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            actor = Actors(
                name='Chris',
                age=35,
                gender='male'
            )
            self.db.session.add(actor)
            self.db.session.commit()
            response = self.client().patch(
                f'/actors/{actor.id}',
                headers={'Authorization': 'Bearer abcd'},
                json={'name': 'Dyna'}
            )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_patch_actors_fail(self, mock_verify_decode, mock_check_perm):
        """ Test PATCH request to actors fail """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        response = self.client().patch(
            f'/actors/1111',
            headers={'Authorization': 'Bearer abcd'},
            json={'name': 'Johson'}
        )
        self.assertEqual(response.status_code, 404)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_detele_actors_pass(self, mock_verify_decode, mock_check_perm):
        """ Test DELETE request to actors pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        with self.app.app_context():
            actor = Actors(
                name='Shankar',
                age=35,
                gender='male'
            )
            self.db.session.add(actor)
            self.db.session.commit()
            response = self.client().delete(
                f'/actors/{actor.id}',
                headers={'Authorization': 'Bearer abcd'}
            )
        data = json.loads(response.data)
        expected_data = {
            'success': True,
            'deleted': actor.id
        }
        self.assertEqual(data, expected_data)
        self.assertEqual(response.status_code, 200)

    @mock.patch('auth.check_permissions')
    @mock.patch('auth.verify_decode_jwt')
    def test_detele_actors_fail(self, mock_verify_decode, mock_check_perm):
        """ Test DELETE request to actors pass """
        mock_verify_decode.return_value = {}
        mock_check_perm.return_value = True
        response = self.client().delete(
            f'/actors/1111',
            headers={'Authorization': 'Bearer abcd'}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

