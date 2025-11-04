"""
app.py
--------

This script initializes the hotel management database and allows
the user to insert hotel and user data through the command line.

Functions:
- Initializes database tables.
- Collects hotel details (name, rooms, location, rating, price).
- Collects user details (after hotel input ends).

Run:
    python app.py
"""


from database_file import init_db, insert_hotel, insert_user


def main():
    # Initialize DB
    init_db()

    print("======= Enter Hotel Data ========")
    while True:
        hotel_name = input("Hotel Name (leave blank to stop): ").strip()
        if not hotel_name:
            print("Now enter User Data!")
            break

        rooms_available = int(input("Rooms Available: "))
        location = input("Location: ").strip()
        rating = float(input("Rating: "))
        price_per_room = float(input("Price per Room: "))

        insert_hotel(hotel_name, rooms_available,
                     location, rating, price_per_room)

    print("\n====== Enter User Data =====")
    while True:
        user_name = input("User Name (leave blank to stop): ").strip()
        if not user_name:
            break
        user_id = input("User ID: ").strip()
        booking_cost = float(input("Booking Cost: "))

        insert_user(user_name, user_id, booking_cost)

    print("\nAll data saved successfully in database!")


if __name__ == "__main__":
    main()
