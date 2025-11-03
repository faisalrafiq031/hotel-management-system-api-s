import sqlite3

# Initialize database


def init_db():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()

    # Create Hotels Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name TEXT,
            rooms_available INTEGER,
            location TEXT,
            rating REAL,
            price_per_room INTEGER    
        )
    ''')

    # Create Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id TEXT,
            booking_cost INTEGER       
        )
    ''')

    conn.commit()
    conn.close()

# Insert hotel data


def insert_hotel(hotel_name, rooms_available, location, rating, price_per_room):
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    c.execute("INSERT INTO hotels (hotel_name, rooms_available, location, rating, price_per_room) VALUES (?, ?, ?, ?, ?)",
              (hotel_name, rooms_available, location, rating, price_per_room))
    conn.commit()
    conn.close()

# Insert user data


def insert_user(user_name, user_id, booking_cost):
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (user_name, user_id, booking_cost) VALUES (?, ?, ?)",
              (user_name, user_id, booking_cost))
    conn.commit()
    conn.close()

# Fetch all hotels data


def fetch_hotels():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hotels")
    data = c.fetchall()
    conn.close()
    return data

# Fetch all users data


def fetch_users():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()
    return data
