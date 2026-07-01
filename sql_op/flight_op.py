#SQL Functions for adding, displaying, modifying and deleting flights

from database import Database

db = Database("FlightBookingSystem")
cursor = db.cursor


def get_flight_by_id(flightID):
    cursor.execute("SELECT * FROM flights WHERE id = %s", (flightID,))
    return cursor.fetchone()

def add_flight(flightID, flightName, maxSeats, seatsAmt):
    cursor.execute(
        "INSERT INTO flights (id, name, maxseats, availableseats, bookedseats, adminpin) VALUES (%s, %s, %s, %s, %s, %s)",
        (flightID, flightName, maxSeats, seatsAmt, '[]', '000000')
    )

def remove_flight(flightID):
    cursor.execute("DELETE FROM flights WHERE id = %s", (flightID,))

def update_flight(flightID, field, value):
    query = f"UPDATE flights SET {field} = %s WHERE id = %s"
    cursor.execute(query, (value, flightID))

def reset_flights():
    cursor.execute(f"UPDATE flights SET availableseats = 0")
    cursor.execute(f"UPDATE flights SET bookedseats = '[]'")
    cursor.execute(f"UPDATE flights SET adminpin = 000000")
    cursor.execute(f"UPDATE flights SET isactive = false")

def update(Flight):
    updated_flight = get_flight_by_id(Flight['id'])
    if updated_flight:
        Flight.update(updated_flight)

