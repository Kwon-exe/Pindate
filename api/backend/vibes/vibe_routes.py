from flask import Blueprint, jsonify, request, current_app
try:
    from ..db_connection import get_db
except (ImportError, ValueError):
    try:
        from backend.db_connection import get_db
    except ImportError:
        from api.backend.db_connection import get_db
from mysql.connector import Error

vibes = Blueprint('vibes', __name__)


# GET /vibes - List all vibe tags
# [Maya-1, Josh-5]
@vibes.route('/', methods=['GET'])
def get_all_vibes():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /vibes')
        # TODO: SELECT * FROM Vibe
        cursor.execute("SELECT 1")
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /vibes - Add a new vibe tag
# [Josh-5]
@vibes.route('/', methods=['POST'])
def create_vibe():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('POST /vibes')
        data = request.get_json()
        # TODO: INSERT INTO Vibe (name) VALUES (%s)
        # get_db().commit()
        return jsonify({"message": "TODO"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /vibes/<id> - Rename a vibe tag
# [Josh-5]
@vibes.route('/<int:vibe_id>', methods=['PUT'])
def update_vibe(vibe_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /vibes/{vibe_id}')
        data = request.get_json()
        # TODO: UPDATE Vibe SET name = %s WHERE vibeId = %s
        # get_db().commit()
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /vibes/<id> - Remove a vibe tag
# [Josh-5]
@vibes.route('/<int:vibe_id>', methods=['DELETE'])
def delete_vibe(vibe_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /vibes/{vibe_id}')
        # TODO: DELETE FROM Vibe WHERE vibeId = %s
        # get_db().commit()
        return jsonify({"message": "TODO"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
