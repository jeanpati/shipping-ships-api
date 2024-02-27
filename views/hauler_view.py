import sqlite3
import json


def create_hauler(hauler_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Hauler (name, dock_id)
            VALUES (?, ?)
            """,
            (hauler_data["name"], hauler_data["dock_id"]),
        )

        rows_added = db_cursor.rowcount
    return True if rows_added > 0 else False


def update_hauler(id, hauler_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Hauler
                SET
                    name = ?,
                    dock_id = ?
            WHERE id = ?
            """,
            (hauler_data["name"], hauler_data["dock_id"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_hauler(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Hauler WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_haulers(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_expand" in url["query_params"]:
            # SQL query for expanded return
            db_cursor.execute(
                """
            SELECT
                h.id,
                h.name,
                h.dock_id,
                d.id dockId,
                d.location dockLocation,
                d.capacity dockCapacity
            FROM Hauler h
            JOIN Dock d
            ON d.id = h.dock_Id
            """
            )
        else:
            # SQL query for unexpanded return
            db_cursor.execute(
                """
            SELECT
                h.id,
                h.name,
                h.dock_id
            FROM Hauler h
            """
            )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        haulers = []
        if "_expand" in url["query_params"]:
            for row in query_results:
                dock = {
                    "id": row["dockId"],
                    "location": row["dockLocation"],
                    "capacity": row["dockCapacity"],
                }
                hauler = {
                    "id": row["id"],
                    "name": row["name"],
                    "dock_id": row["dock_id"],
                    "dock": dock,
                }
                haulers.append(hauler)
        else:
            for row in query_results:
                hauler = {
                    "id": row["id"],
                    "name": row["name"],
                    "dock_id": row["dock_id"],
                }
                haulers.append(hauler)
        # Serialize Python list to JSON encoded string
        serialized_haulers = json.dumps(haulers)

    return serialized_haulers


def retrieve_hauler(pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            h.id,
            h.name,
            h.dock_id
        FROM Hauler h
        WHERE h.id = ?
        """,
            (pk,),
        )
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_hauler = json.dumps(dict(query_results))

    return serialized_hauler
