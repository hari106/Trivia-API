import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import test

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        DB_USER = os.getenv('DB_USER', 'postgres')  
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        DB_NAME = os.getenv('DB_NAME', 'trivia_test')  
        DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/api/v1.0/categories")
        data = json.loads(res.data)
        
        self.assertIn('categories', data)
        self.assertTrue(len(data['categories']))

    def test_get_category_by_id(self):
        res = self.client().get('/api/v1.0/categories/2')
        data = json.loads(res.data)

        self.assertNotEqual(data['id'], None)
        self.assertNotEqual(data['type'], None)

    def test_get_category_by_id_missing(self):
        res = self.client().get('/api/v1.0/categories/-1')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
        self.assertEqual(data['error'], 404)

    def test_get_questions(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)

        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)
        self.assertIn('categories', data)

        self.assertTrue(len(data['questions']) >= 0)
        self.assertTrue(len(data['categories']) >= 0)
        self.assertTrue(data['totalQuestions'] >= 0)

    def test_get_questions_exceed_page(self):
        res = self.client().get('/api/v1.0/questions?page=2000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
        self.assertEqual(data['error'], 404)

    def test_post_questions(self):
        test_data = {
            'question': 'What is the first natural prime number ?',
            'answer': '2',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().post('/api/v1.0/questions', json=test_data)
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.question == test_data['question'],
            Question.category == test_data['category'],
            Question.difficulty == test_data['difficulty'],
            Question.answer == test_data['answer']
            ).one_or_none()

        self.assertNotEqual(question, None)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Added successfully')

    def test_delete_question(self):
        res = self.client().delete('/api/v1.0/questions/5')
        data = json.loads(res.data)

        deleted = Question.query.get(5)

        self.assertEqual(deleted, None)
        self.assertEqual(data['statusCode'], 200)
        self.assertEqual(data['id'], 5)

    def test_post_questions_wrong_endpoint(self):
        test_data = {
            'question': 'What is the first natural prime number ?',
            'answer': '2',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().post('/api/v1.0/questions/2', json=test_data)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Method not allowed')
        self.assertEqual(data['error'], 405)

    def test_search_questions_by_term(self):
        search_txt = {
            'searchTerm': 'actor'
        }

        res = self.client().post('/api/v1.0/questions', json=search_txt)
        data = json.loads(res.data)

        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)
        self.assertTrue(data['totalQuestions'] >= 0)

    def test_search_questions_by_term_fail(self):
        search_txt = {
            'searchTerm': 'xyzhskd'
        }

        res = self.client().post('/api/v1.0/questions', json=search_txt)
        data = json.loads(res.data)

        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)
        self.assertTrue(data['totalQuestions'] == 0)

    def test_post_quizzes(self):
        test_data = {
            'previous_questions': [15,19],
            'quiz_category': 'Art'
        }

        res = self.client().post('/api/v1.0/quizzes', json=test_data)
        data = json.loads(res.data)

        self.assertIn('question', res.data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()