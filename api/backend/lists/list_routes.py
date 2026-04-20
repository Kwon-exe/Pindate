from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

lists = Blueprint('lists', __name__)


# All list IDs [Maya-2]
@lists.route('/', methods=['GET'])
def get_all_lists():
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


# Create a new empty list [Maya-2]
# Implemented on users blueprint: POST /users/<user_id>/lists
@lists.route('/', methods=['POST'])
def create_list():
    return jsonify({"error": "Use POST /users/<user_id>/lists to create a list"}), 410


# Venues in a specific list [Maya-2]
@lists.route('/<int:list_id>', methods=['GET'])
def get_list(list_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT v.venueId, v.name, v.rating, v.address, v.city,
                   v.minPrice, v.maxPrice
            FROM ListVenue lv
            JOIN Venues v ON v.venueId = lv.venueId
            WHERE lv.listId = %s
            ORDER BY v.name
            """,
            (list_id,),
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Add a venue to a list [Maya-2]
@lists.route('/<int:list_id>/venues', methods=['POST'])
def add_venue_to_list(list_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        venue_id = data.get('venueId')
        if not venue_id:
            return jsonify({"error": "'venueId' is required"}), 400

        cursor.execute(
            "INSERT INTO ListVenue (listId, venueId) VALUES (%s, %s)",
            (list_id, venue_id),
        )
        get_db().commit()
        return jsonify({"message": "Venue added to list"}), 201
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        if e.errno == 1062:
            return jsonify({"error": "Venue already in list"}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Remove a venue from a list [Maya-2]
@lists.route('/<int:list_id>/venues', methods=['DELETE'])
def remove_venue_from_list(list_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json(silent=True) or {}
        venue_id = data.get('venueId')
        if not venue_id:
            return jsonify({"error": "'venueId' is required"}), 400

        cursor.execute(
            "DELETE FROM ListVenue WHERE listId = %s AND venueId = %s",
            (list_id, venue_id),
        )
        get_db().commit()
        return jsonify({"message": "Venue removed from list"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a list [Maya-2]
@lists.route('/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM ListVenue WHERE listId = %s", (list_id,))
        cursor.execute("DELETE FROM Lists WHERE listId = %s", (list_id,))
        get_db().commit()
        return jsonify({"message": "List deleted"}), 200
    except Error as e:
        current_app.logger.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
