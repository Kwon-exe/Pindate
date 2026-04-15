from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

users = Blueprint('users', __name__)


# List users with info [Josh-2]
@users.route('/', methods=['GET'])
def get_all_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Register a new user [Maya]
@users.route('/', methods=['POST'])
def create_user():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get user profile [Maya]
@users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update user info [Maya]
@users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
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


# Ban / delete a user account [Josh-2]
@users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
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


# All reviews written by a user [Maya-3, Marcus-4]
@users.route('/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# All flagged reviews by a specific user [Josh-2]
@users.route('/<int:user_id>/flagged-reviews', methods=['GET'])
def get_user_flagged_reviews(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# All lists created by a user [Maya-2]
@users.route('/<int:user_id>/lists', methods=['GET'])
def get_user_lists(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new named list for user [Maya-2]
@users.route('/<int:user_id>/lists', methods=['POST'])
def create_user_list(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# User's saved venues with save date [Maya-5]
@users.route('/<int:user_id>/saved', methods=['GET'])
def get_saved_venues(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Save a venue to user's saved list [Maya-5]
@users.route('/<int:user_id>/saved', methods=['POST'])
def save_venue(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Remove a venue from saved list [Maya-5]
@users.route('/<int:user_id>/saved', methods=['DELETE'])
def unsave_venue(user_id):
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


# All venues the user has marked visited [Maya-5]
@users.route('/<int:user_id>/visited', methods=['GET'])
def get_visited_venues(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # TODO: complete query
        cursor.execute("SELECT 1")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Mark a venue as visited [Maya-5]
@users.route('/<int:user_id>/visited', methods=['POST'])
def mark_visited(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        # TODO: complete query
        get_db().commit()
        return jsonify({"message": "TODO"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Unmark a venue as visited [Maya-5]
@users.route('/<int:user_id>/visited', methods=['DELETE'])
def unmark_visited(user_id):
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
