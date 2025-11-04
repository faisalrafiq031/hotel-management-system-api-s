"""
queries.py
------------

This module contains SQL query functions for retrieving and sorting
hotel and user data from the 'Hotel_Management_System.db' database.

Functions:
- show_all_hotels(): Display all hotel records.
- sort_hotels_by_name(): Sort and show hotels alphabetically.
- sort_hotels_by_rating(): Sort and show hotels by highest rating.
- show_hotels_in_specific_location(): Show hotels filtered by 'Lahore'.
- sort_hotels_by_rooms(): Sort and show hotels by maximum rooms available.
- show_users(): Display all user records from the database.

Run:
    python queries.py
"""


import sqlite3


def show_all_hotels():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM hotels"):
        print(row)
    conn.close()


def sort_hotels_by_name():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM hotels ORDER BY hotel_name ASC"):
        print(row)
    conn.close()


def sort_hotels_by_rating():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM hotels ORDER BY rating DESC"):
        print(row)
    conn.close()


def show_hotels_in_specific_location():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM hotels WHERE location = 'Lahore'"):
        print(row)
    conn.close()


def sort_hotels_by_rooms():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM hotels ORDER BY rooms_available DESC"):
        print(row)
    conn.close()


def show_users():
    conn = sqlite3.connect('Hotel_Management_System.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM users"):
        print(row)
    conn.close()


if __name__ == "__main__":
    print("All Hotel Data:")
    show_all_hotels()

    print("\nSorted by Name:")
    sort_hotels_by_name()

    print("\nSorted by Highest Rating:")
    sort_hotels_by_rating()

    print("\nHotels in specific location 'Lahore':")
    show_hotels_in_specific_location()

    print("\nSorted by Maximum Rooms:")
    sort_hotels_by_rooms()

    print("\nUser Booking Data:")
    show_users()
