import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import NotFound
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    """
    Main flask function to create the app object
    """
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        """
        public end point to get the categories
        """
        return jsonify(
            {
                "success": True,
                "categories": {
                    category.id: category.type
                    for category in Category.query.all()
                }
            }
        ), 200

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination
    at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        public end point to get the questions
        """
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()[start:end]
        if not questions:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": list(
                    map(lambda question: question.format(), questions)),
                "total_questions": len(Question.query.all()),
                "categories": {
                    category.id: category.type
                    for category in Category.query.all()
                },
                "current_category": ""
            }

        ), 200
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def question_delete(id):
        """
        end point to delete question by id
        """
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({"success": True, "delete": id}), 200
        except NotFound:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and
    the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    def search_and_add_questions():
        """
        end point for search and add new question
        """
        search = request.json.get("searchTerm", None)
        if search:
            questions = Question.query.filter(
                Question.question.ilike("%{}%".format(search)))
            return jsonify({
                "success": True,
                "questions": list(
                    map(lambda question: question.format(),
                        questions)),

                "total_questions": len(questions.all()),
                "categories": {
                    category.id: category.type
                    for category in Category.query.all()
                },
                "current_category": ""
            }), 200
        else:
            question = Question(**request.json)
            question.insert()
            return jsonify({
                "success": True,
                "question": question.format()
            }), 200

    # made add and search in one end_point according to frontend

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<id>/questions', methods=['GET'])
    def get_category_questions(id):
        """
        public end point to get the questions by category
        """
        if int(id) not in [category.id
                           for category in Category.query.all()]:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": list(
                    map(lambda question: question.format(),
                        Question.query.filter_by(category=id))),
                #  we don't have pagination in this end_point
                "total_questions": len(Question.query.filter(
                    Question.category == id).all()),
                "categories": {
                    category.id: category.type
                    for category in Category.query.all()
                },
                # no use for this field in the frontend
                "current_category": Category.query.filter(
                    Category.id == id).one_or_none().type
            }

        ), 200

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        """
        end point to "Play" tab and quizz
        """
        try:
            previous_questions = request.json.get("previous_questions", None)
            quiz_category = request.json.get("quiz_category", None)
            questions = Question.query
            if int(quiz_category.get('id')):
                questions = Question.query.filter_by(
                    category=str(quiz_category.get('id')))
            return jsonify(
                {
                    "success": True,
                    "question": questions.filter(
                        Question.id.notin_(
                            previous_questions)).first().format()
                }
            ), 200
        except AttributeError:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        '''
        error handling for unprocessable entity
        '''
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        '''
        implement error handler for 404
        '''
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    return app
