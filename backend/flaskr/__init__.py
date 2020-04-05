import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def paginate_questions(request, query):
        page = request.args.get("page", 1, type=int)
        paginate = query.paginate(page, QUESTIONS_PER_PAGE)
        questions = [i.format() for i in paginate.items]
        return questions, paginate.total

    @app.route("/categories")
    def get_all_categories():
        categories = {c.id: c.type for c in Category.query.all()}

        return jsonify({"success": True, "categories": categories, })

    @app.route("/questions")
    def get_paginated_questions():
        categories = {c.id: c.type for c in Category.query.all()}
        current_questions, total = paginate_questions(request, Question.query)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total,
                "current_category": None,
                "categories": categories,
            }
        )

    @app.route("/questions", methods=["POST"])
    def add_new_question():
        body = request.get_json()

        # If this request is for searcing questions
        if "searchTerm" in body:
            try:
                searchTerm = body["searchTerm"]
                questions = Question.query.filter(
                    Question.question.ilike("%{}%".format(searchTerm))
                )
                current_questions, total = paginate_questions(
                    request, questions)
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": total,
                        "current_category": None,
                    }
                )
            except Exception as ex:
                print(ex)
                abort(422)
        else:
            try:
                question = Question(
                    question=body["question"],
                    answer=body["answer"],
                    category=body["category"],
                    difficulty=body["difficulty"],
                )
                question.insert()
                current_questions, total = paginate_questions(
                    request, Question.query)
                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": total,
                    }
                )
            except Exception as ex:
                print(ex)
                abort(422)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).first_or_404()
            question.delete()

            return jsonify({"success": True, "deleted_id": question_id, })
        except Exception as ex:
            print(ex)
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def get_paginated_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id)
        current_questions, total = paginate_questions(request, selection)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total,
                "current_category": category_id,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def quiz():
        body = request.get_json()

        try:
            previous_question_ids = body["previous_questions"]
            quiz_category = body["quiz_category"]

            questions = []
            if quiz_category["id"] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category["id"]).all()
            previous_questions = [
                Question.query.get(q_id) for q_id in previous_question_ids
            ]
            for pq in previous_questions:
                if pq in questions:
                    questions.remove(pq)

            current = None
            if len(questions) != 0:
                random.shuffle(questions)
                current = questions[0].format()

            return jsonify({"success": True, "question": current, })
        except Exception as ex:
            print(ex)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False, "error": 400, "message": "Bad request"}
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "Not found"
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable entity"
                }
            ), 422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Server error"
                }
            ), 500,
        )

    return app
