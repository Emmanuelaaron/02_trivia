import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:comforter@{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEquals(data["message"], "resource not found")

    def test_create_question(self):
        question = {
            "question": "who are you?",
            "answer": "i am who iam",
            "category": 1,
            "diffculty": 4
        }
        resp = self.client().post("/questions", content_type="application/json", data=json.dumps(question))
        self.assertEqual(resp.status_code, 422)

    def test_search_question(self):
        question = {
            "question": "who"
        }
        resp = self.client().post('/questions/search', content_type="application/json", data=json.dumps(question))
        self.assertEquals(resp.status_code, 404)

    def test_get_by_category(self):
        resp = self.client().get('/categories/4/questions')
        self.assertEqual(resp.status_code, 500)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()