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
        self.username = "postgres"
        self.password = "password"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.username,
            self.password,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "1+1",
            "answer": "2",
            "difficulty": 1,
            "category": 1
        }
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
    Write at least one test for each test
     for successful operation and for expected errors.
    """

    def test_get_question(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))
        self.assertGreater(int(data['total_questions']), 0)

    def test_get_paginated_question(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))
        self.assertGreater(int(data['total_questions']), 0)

    def test_404_sent_request(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_valid_question_search(self):
        res = self.client().post("/questions", json={"searchTerm": "what"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertGreater(int(data['total_questions']), 0)

    def test_invalid_question_search(self):
        res = self.client().post("/questions",
                                 json={
                                     "searchTerm":
                                     "3232WER#$R$#FRGRHHSwefewgD"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['questions'])
        self.assertFalse(len(data['questions']))
        self.assertEqual(int(data['total_questions']), 0)

    def test_add_new_question(self):
        count = len(Question.query.all())
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(count+1, len(Question.query.all()))

    def test_delete_question(self):
        count = len(Question.query.all())
        question_id = Question.query.all()[-1].id
        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], question_id)
        self.assertEqual(count-1, len(Question.query.all()))

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["current_category"], "Science")
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))
        self.assertGreater(int(data['total_questions']), 0)
        self.assertLess(int(data['total_questions']),
                        len(Question.query.all()))

    def test_get_invalid_category_questions(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question_invalid_id(self):
        res = self.client().delete("questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_quiz_question(self):
        res = self.client().post("/quizzes",
                                 json={
                                     "previous_questions": [5],
                                     "quiz_category": {
                                         "type": "Science",
                                         "id": 4
                                     },
                                 },
                                 content_type='application/json'
                                 )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_invalid_get_quiz_question(self):
        """
        invalid request: send request without json data
        """
        res = self.client().post("/quizzes")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_method_not_allowed(self):
        """
        invalid request: send request without json data
        """
        res = self.client().get("/quizzes")
        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
