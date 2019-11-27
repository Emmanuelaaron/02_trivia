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
        self.database_path = "postgres://postgres:comforter@{}/{}".format(
            'localhost:5432', self.database_name)
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

    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("categories", data)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("categories", data)

    def test_delete_question_not_found(self):
        res = self.client().delete("/questions/167676")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEquals(data["message"], "resource not found")
    
    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Question deleted", data)

    def test_create_question(self):
        question = {
            "question": "who are you?",
            "answer": "i am who iam",
            "category": 1,
            "difficulty": 4
        }
        resp = self.client().post("/questions", content_type="application/json",
                                  data=json.dumps(question))
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEquals(reply["message"], "question created succesfully")
    
    def test_create_question_unprocessable(self):
        question = {
            "question": "gshg",
            "unprocessable": "wapi"
        }
        resp = self.client().post("/questions", content_type="application/json",
                                  data=json.dumps(question))
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 422)
        self.assertEquals(reply["message"], "unprocessable")

    def test_search_question(self):
        question = {
            "question": "who"
        }
        resp = self.client().post('/questions/search',
                                  content_type="application/json", data=json.dumps(question))
        data = json.loads(resp.data.decode())
        self.assertEquals(resp.status_code, 200)
        self.assertIn("questions", data)

    def test_search_question_not_found(self):
        question = {
            "question": "whhghashfhafo"
        }
        resp = self.client().post('/questions/search',
                                  content_type="application/json", data=json.dumps(question))
        data = json.loads(resp.data.decode())
        self.assertEquals(resp.status_code, 404)
        self.assertIn("resource not found", str(data))

    def test_get_quiz_questions(self):
        category = {
            "quiz_category": 1
        }

        previous = {
            "previous_questions": "" 
        }
        resp = self.client().post('/quizz',
                                  content_type="application/json", data=json.dumps(category))
        data = json.loads(resp.data.decode())
        print(data)
        self.assertEquals(resp.status_code, 404)

    def test_get_by_category_not_found(self):
        resp = self.client().get('/categories/10/questions')
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)

    def test_get_by_category(self):
        resp = self.client().get('/categories/4/questions')
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)

    def test_get_paginated_questions(self):
        resp = self.client().get('/questions')
        data= json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
