import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      formatted_categories = [category.type for category in Category.query.all()]
      return jsonify({
        'success': True,
        'categories': formatted_categories,
        'total_categories': len(formatted_categories)
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    questions = Question.query.all()
    formated_questions = [question.format() for question in questions]
    formatted_categories = [category.type for category in Category.query.all()]
    return jsonify({
      "success": True,
      "questions": formated_questions[start: end],
      "categories": formatted_categories,
      "total_questions": len(formated_questions)
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    question_to_be_deleted = Question.query.filter_by(id=question_id).first()
    if question_to_be_deleted is None:
      abort(404)
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return jsonify({
      "success": True,
      "Question deleted": question_to_be_deleted.question
    })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions", methods=["POST"])
  def create_question():
    error = False
    body = {}
    try:
      data = request.get_json()
      question = data["question"]
      answer_text = data["answer"]
      category = data["category"]
      difficulty = data["difficulty"]
      question_created = Question(
        question=question, 
        answer=answer_text, 
        category=category, 
        difficulty=difficulty
        )
      db.session.add(question_created)
      db.session.commit()
      body["question"] = question
      body["answer"] = answer_text
      body["category"] = category
      body["difficulty"] = difficulty 
    except:
      error = True
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()
    if not error:
      return jsonify({
        "success": True,
        "body": body,
        "message": "question created succesfully"

      }), 201
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=["POST"])
  def get_search_item():
    question = request.get_json()["question"]
    question = "%{}%".format(question)
    questions = Question.query.filter(Question.question.like(question)).all()
    if not questions:
      abort(404)
    return jsonify({
      "questions": [question.format() for question in questions],
      "total_questions": len(questions),
      "categories": [item.type for item in Category.query.all()]
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions")
  def get_by_category(category_id):
    my_questions = Question.query.filter_by(category=category_id).all()
    if not my_questions:
      abort(404)
    current_category = Category.query.filter_by(id=category_id).first().format()
    return jsonify({
      "questions": [question.format() for question in my_questions],
      "total_questions": len(my_questions),
      "current_category": current_category
    })

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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422
  
  return app

    