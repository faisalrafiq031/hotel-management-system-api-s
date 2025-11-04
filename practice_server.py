"""
practice_Server.py
------------------

This module implements a simple RESTful API using Python's built-in `http.server`
for managing hotel and user data in the 'Hotel_Management_System.db' SQLite database.

Features:
- Handle CRUD operations for Hotels and Users.
- Supports GET, POST, PUT, DELETE methods.
- Implements CORS headers for browser compatibility.
- Dynamic routes for sorting, filtering, and location-based queries.

Classes:
- Building_api_requests: Handles incoming HTTP requests and routes them accordingly.

Functions:
- get_database_connection(): Returns an active SQLite connection.
- run(): Starts the HTTP server on the specified port (default: 5000).

Usage:
    python practice_Server.py
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
from urllib.parse import urlparse, unquote

Database_name = "Hotel_Management_System.db"


def get_database_connection():
    return sqlite3.connect(Database_name)


class Building_api_requests(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)

        # Standard headers
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # used to handle preflight requests from browsers for CORS policy compliance
    def do_OPTIONS(self):
        self._set_headers()

    # DO GET Method to handle GET requests for Hotels and Users
    def do_GET(self):
        path = self.path

        if path == "/":
            self._set_headers()
            routes_info = {
                "message": "Welcome to the Hotel Management System API",

                "Hotel_Routes": {
                    "Get all hotels": "GET /hotels",
                    "Add hotel": "POST /hotels/add",
                    "Update hotel": "PUT /hotels/update/<id>",
                    "Delete hotel": "DELETE /hotels/delete/<id>",
                    "Get by location": "GET /hotels/location/<city>",
                    "Sort hotels": "GET /hotels/sort/<type>"
                },
                "User_Routes": {
                    "Get all users": "GET /users",
                    "Add user": "POST /users/add",
                    "Update user": "PUT /users/update/<id>",
                    "Delete user": "DELETE /users/delete/<id>",
                    "Booking Cost": "GET /users/booking_cost/<user_id>"
                }
            }
            self.wfile.write(json.dumps(routes_info, indent=4).encode())
            return

        # ROUTES for fetching all Hotels Data
        if path == "/hotels":
            conn = get_database_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM hotels")
            # Fetch all hotels and format as list of dicts
            fetch_hotel_data = [dict(
                id=row[0], hotel_name=row[1], rooms_available=row[2],
                location=row[3], rating=row[4], price_per_room=row[5]
            ) for row in c.fetchall()]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(fetch_hotel_data).encode())

        # ROUTES for fetching Hotels by Location
        elif path.startswith("/hotels/location/"):
            location = unquote(path.split("/")[-1])
            conn = get_database_connection()
            c = conn.cursor()

            c.execute("SELECT * FROM hotels WHERE location = ?", (location,))
            rows = c.fetchall()

            if not rows:
                self._set_headers(404)
                self.wfile.write(json.dumps(
                    {"error": f"No hotels found in location '{location}'."}).encode())
                conn.close()
                return

            # Fetch all hotels and format as list of dicts
            fetch_hotel_data = [dict(
                id=row[0], hotel_name=row[1], rooms_available=row[2],
                location=row[3], rating=row[4], price_per_room=row[5]
            ) for row in rows]

            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(fetch_hotel_data).encode())

        # ROUTES for sorting Hotels
        elif path.startswith("/hotels/sort/"):
            sort_type = path.split("/")[-1]
            conn = get_database_connection()
            c = conn.cursor()

            if sort_type == "name":
                c.execute("SELECT * FROM hotels ORDER BY hotel_name ASC")
            elif sort_type == "rating":
                c.execute("SELECT * FROM hotels ORDER BY rating DESC")
            elif sort_type == "rooms":
                c.execute("SELECT * FROM hotels ORDER BY rooms_available DESC")
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps(
                    {"error": "Invalid sort type. Use 'name', 'rating', or 'rooms'."}).encode())
                return

            # Fetch all hotels and format as list of dicts
            fetch_hotel_data = [dict(
                id=row[0], hotel_name=row[1], rooms_available=row[2],
                location=row[3], rating=row[4], price_per_room=row[5]
            ) for row in c.fetchall()]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(fetch_hotel_data).encode())

        # ROUTES for fetching Users Data
        elif path == "/users":
            conn = get_database_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users")

            # Fetch all users and format as list of dicts
            fetch_user_data = [dict(
                id=row[0], user_name=row[1], user_id=row[2],
                booking_cost=row[3]
            ) for row in c.fetchall()]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(fetch_user_data).encode())

        # ROUTES for fetching Users Booking Cost
        elif path == "/users/booking_cost":
            conn = get_database_connection()
            c = conn.cursor()
            c.execute("SELECT user_id, booking_cost FROM users")

            # Fetch all users' booking costs and format as list of dicts
            fetch_booking_data = [dict(
                user_id=row[0], booking_cost=row[1]
            ) for row in c.fetchall()]
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(fetch_booking_data).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps(
                {"error": "Route not found. Please Check if exist."}).encode())

    # Add Data using POST Method
    def do_POST(self):
        self.content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(self.content_length)
        data = json.loads(post_data)
        path = self.path

        if path == "/hotels/add":
            try:
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT id FROM hotels WHERE hotel_name = ? AND location = ?",
                          (data['hotel_name'], data['location']))
                existing_hotel = c.fetchone()

                if existing_hotel:
                    self._set_headers(400)
                    self.wfile.write(json.dumps(
                        {"error": f"Hotel '{data['hotel_name']}' already exists in {data['location']}."}).encode())
                else:
                    c.execute("""INSERT INTO hotels (hotel_name, rooms_available, location, rating, price_per_room)
                              VALUES (?, ?, ?, ?, ?)""",
                              (data['hotel_name'], data['rooms_available'], data['location'], data['rating'], data['price_per_room']))
                    conn.commit()
                    self.wfile.write(json.dumps(
                        {"message": "Hotel added successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps(
                    {"error": f"Database connection error: {str(e)}"}).encode())
                return
            finally:
                conn.close()

        elif path == "/users/add":
            try:
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT id FROM users WHERE user_id = ?",
                          (data['user_id'],))
                existing_user = c.fetchone()

                if existing_user:
                    self._set_headers(400)
                    self.wfile.write(json.dumps(
                        {"error": f"User with ID '{data['user_id']}' already exists."}).encode())
                else:
                    c.execute("""INSERT INTO users (user_name, user_id, booking_cost)
                              VALUES (?, ?, ?)""",
                              (data['user_name'], data['user_id'], data['booking_cost']))
                    conn.commit()
                    self.wfile.write(json.dumps(
                        {"message": "User added successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps(
                    {"error": f"Database connection error: {str(e)}"}).encode())
                return
            finally:
                conn.close()

    def do_PUT(self):
        self.content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(self.content_length)
        data = json.loads(post_data)
        path = self.path

        if path.startswith("/hotels/update/"):
            try:
                hotel_id = int(path.split("/")[-1])
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT * FROM hotels WHERE id = ?", (hotel_id,))
                existing = c.fetchone()

                if not existing:
                    self._set_headers(404)
                    self.wfile.write(json.dumps(
                        {"error": f"Hotel with ID '{hotel_id}' not found."}).encode())
                    return

                # Build update fields dynamically
                fields = []
                values = []
                for key in ["hotel_name", "rooms_available", "location", "rating", "price_per_room"]:
                    if key in data:
                        fields.append(f"{key} = ?")
                        values.append(data[key])

                if not fields:
                    self._set_headers(400)
                    self.wfile.write(json.dumps(
                        {"error": "No valid fields to update."}).encode())
                    return

                values.append(hotel_id)
                query = f"UPDATE hotels SET {', '.join(fields)} WHERE id = ?"
                c.execute(query, values)
                conn.commit()

                self._set_headers(200)
                self.wfile.write(json.dumps(
                    {"message": f"Hotel with ID '{hotel_id}' has updated successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            finally:
                conn.close()

        if path.startswith("/users/update/"):
            try:
                user_id = int(path.split("/")[-1])
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                existing = c.fetchone()

                if not existing:
                    self._set_headers(404)
                    self.wfile.write(json.dumps(
                        {"error": f"User with ID '{user_id}' not found."}).encode())
                    return
                # Build update fields dynamically
                fields = []
                values = []
                for key in ["user_name", "user_id", "booking_cost"]:
                    if key in data:
                        fields.append(f"{key} = ?")
                        values.append(data[key])

                if not fields:
                    self._set_headers(400)
                    self.wfile.write(json.dumps(
                        {"error": "No valid fields to update."}).encode())
                    return

                values.append(user_id)
                query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
                c.execute(query, values)
                conn.commit()

                self._set_headers(200)
                self.wfile.write(json.dumps(
                    {"message": f"User with ID '{user_id}' has updated successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            finally:
                conn.close()

    def do_DELETE(self):
        path = self.path

        if path.startswith("/hotels/delete/"):
            try:
                hotel_id = int(path.split("/")[-1])
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT * FROM hotels WHERE id = ?", (hotel_id,))
                existing = c.fetchone()

                if not existing:
                    self._set_headers(404)
                    self.wfile.write(json.dumps(
                        {"error": f"Hotel with ID '{hotel_id}' not found."}).encode())
                    return

                c.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))
                conn.commit()

                self._set_headers(200)
                self.wfile.write(json.dumps(
                    {"message": f"Hotel with ID '{hotel_id}' has been deleted successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            finally:
                conn.close()

        if path.startswith("/users/delete/"):
            try:
                user_id = int(path.split("/")[-1])
                conn = get_database_connection()
                c = conn.cursor()

                c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                existing = c.fetchone()

                if not existing:
                    self._set_headers(404)
                    self.wfile.write(json.dumps(
                        {"error": f"User with ID '{user_id}' not found."}).encode())
                    return

                c.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()

                self._set_headers(200)
                self.wfile.write(json.dumps(
                    {"message": f"User with ID '{user_id}' has been deleted successfully."}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            finally:
                conn.close()


def run(server_class=HTTPServer, handler_class=Building_api_requests, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on http://127.0.0.1:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
