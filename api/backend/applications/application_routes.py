from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

applications = Blueprint('applications', __name__)


# List all applications (filterable by status) [Josh-3]
@applications.route('/', methods=['GET'])
def get_all_applications():
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


# Submit a new venue application [Marcus-5]
@applications.route('/', methods=['POST'])
def create_application():
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


# Full details of an application [Josh-3]
@applications.route('/<int:app_id>', methods=['GET'])
def get_application(app_id):
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


# Approve or reject an application [Josh-3]
@applications.route('/<int:app_id>', methods=['PUT'])
def update_application(app_id):
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
