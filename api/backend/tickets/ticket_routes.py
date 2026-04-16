from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

tickets = Blueprint('tickets', __name__)


# List all open report tickets [Josh-1]
@tickets.route('/', methods=['GET'])
def get_all_tickets():
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


# Submit a new report ticket [Marcus-3]
@tickets.route('/', methods=['POST'])
def create_ticket():
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


# Detail view of a specific ticket [Josh-1]
@tickets.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
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


# Resolve, dismiss, or escalate a ticket [Josh-1]
@tickets.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
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
