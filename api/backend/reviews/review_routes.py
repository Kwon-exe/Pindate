from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

reviews = Blueprint('reviews', __name__)


# Get a specific review [Maya-4]
@reviews.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Edit own review [Maya-3]
@reviews.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete own review [Maya-3]
@reviews.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Flag a review as inappropriate [Marcus-3, Josh-1]
@reviews.route('/<int:review_id>/flag', methods=['POST'])
def flag_review(review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
