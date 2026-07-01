#SQL Functions for adding, displaying, modifying and deleting bookings

from database import connection, cursor
from datetime import datetime
from generate_random_id import generate_random_id


def get_bookings():
    cursor.execute("SELECT * FROM bookings")
    return cursor.fetchall()

def select_booking(bookingID):
    cursor.execute("SELECT * FROM bookings WHERE id = %s", (bookingID,))
    return cursor.fetchone()

def add_booking(travelDate, departure, arrival, passengers, flightID):
    booking_ids = [booking['id'] for booking in get_bookings()]
    cursor.execute(
        "INSERT INTO bookings (id, date, traveldate, departingfrom, arrivingat, passengers, flightid, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (generate_random_id(8, booking_ids), datetime.now().strftime("%x"), travelDate, departure, arrival, passengers, flightID, True)
    )

def remove_booking(bookingID):
    cursor.execute("DELETE FROM bookings WHERE id = %s", (bookingID,))

def update_booking(bookingID, field, value):
    query = f"UPDATE bookings SET {field} = %s WHERE id = %s"
    cursor.execute(query, (value, bookingID))

def clear_bookings():
    cursor.execute(f"DELETE FROM bookings")

def update(booking):
    updated_booking = select_booking(booking['id'])
    if updated_booking:
        booking.update(updated_booking)


# TESTING AREA:
#--------------------------------------------

#type a command...

