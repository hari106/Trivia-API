import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_req(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')

        return response

    @app.route('/api/v1.0/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        formatted_cats = [category.format() for category in categories]

        return jsonify({'categories': formatted_cats})

    @app.route('/api/v1.0/categories/<int:cat_id>', methods=['GET'])
    def get_category_by_id(cat_id):
        category = Category.query.get(cat_id)

        if category is None:
            abort(404)

        return jsonify(category.format())

    @app.route('/api/v1.0/questions', methods=['GET'])
    def get_questions():
        page_num = request.args.get('page', 1, int)
        start = page_num - 1
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        categories = Category.query.all()

        count = len(questions)

        if page_num > count - 1 or page_num < 1:
            abort(404)

        formatted_questions = [question.format() for question in questions]
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'questions': formatted_questions[start:end],
            'totalQuestions': count,
            'categories': formatted_categories,
        })

    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        status = 200

        if question is None:
            abort(404)

        try:
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
            status = 500
        finally:
            db.session.close()

        return jsonify({
            'statusCode': status,
            'id': question_id
        })

    @app.route('/api/v1.0/questions', methods=['POST'])
    def process_question():
        json_data = json.loads(request.data)
        if 'searchTerm' in json_data:
            searchTerm = json_data['searchTerm']

            questions = Question.query.filter(
                Question.question.ilike('%' + searchTerm + '%'))

            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'questions': formatted_questions,
                'totalQuestions': len(Question.query.all())
            })
        else:
            question_str = json_data['question']
            answer_str = json_data['answer']
            diff_str = json_data['difficulty']
            category_str = json_data['category']

            status = 200
            try:
                question = Question(question_str, answer_str,
                                    category_str, diff_str)
                db.session.add(question)
                db.session.commit()

            except:
                db.session.rollback()
                status = 500
            finally:
                db.session.close()

            if status != 200:
                abort(status)
            
            return jsonify({
              "success": True,
              "message": "Added successfully"
            })


    @app.route('/api/v1.0/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        cat = Category.query.get(category_id)
        print(cat.format())

        if cat is None:
            abort(404)

        questions = Question.query.filter(
            Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.all()),
            'currentCategory': cat.type
        })

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_quizzes():
        json_data = json.loads(request.data)

        prev_questions = json_data['previous_questions']
        category_str = json_data['quiz_category']

        category = Category.query.filter(Category.type == category_str).one()
        questions = Question.query.filter(Question.id not in prev_questions, Question.category == category.id)

        formatted = [question.format() for question in questions]

        index = random.randint(0, len(formatted) - 1)

        return jsonify({'question': formatted[index]})

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        "success": False,
        "error": 404, 
        "message": "Not Found"
      })

    @app.errorhandler(405)
    def not_allowed(error):
      return jsonify({
        "success": False,
        "error": 405, 
        "message": "Method not allowed"
      })

    @app.errorhandler(422)
    def not_processible(error):
      return jsonify({
        "success": False,
        "error": 422, 
        "message": "Unprocessible entity"
      })

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400, 
        "message": "Bad Request"
      })

    @app.errorhandler(500)
    def server_error(error):
      return jsonify({
        "success": False,
        "error": 500, 
        "message": "Internal Server Error"
      })

    return app
