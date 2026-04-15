from flask import Blueprint, jsonify, request, current_app
try:
    from ..db_connection import get_db
except (ImportError, ValueError):
    try:
        from backend.db_connection import get_db
    except ImportError:
        from api.backend.db_connection import get_db
from mysql.connector import Error

admin_log = Blueprint('admin_log', __name__)


# GET /log - Most recent admin actions across platform
# [Josh-6]
@admin_log.route('/', methods=['GET'])
def get_log_entries():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /log')
        # TODO: SELECT from AdminLog JOIN Users ORDER BY performedAt DESC
        cursor.execute("SELECT 1")
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /log/<id> - Detail view of a specific log entry
# [Josh-6]
@admin_log.route('/<int:log_id>', methods=['GET'])
def get_log_entry(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /log/{log_id}')
        # TODO: SELECT from AdminLog JOIN Users WHERE logId = %s
        cursor.execute("SELECT 1")
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
