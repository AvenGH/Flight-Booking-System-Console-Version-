import datacomp as dc
from database import Database
import sql_op.flight_op as flight_op
import json

db = Database("FlightBookingSystem")


def selectFlight(flightID):
    flight = flight_op.get_flight_by_id(flightID)
    if flight:
        return flight


def addFlight():
    flightID = input("Enter the flight ID: ")
    if not dc.is_positive_int(flightID):
        print("Flight ID must only consist of digits.")
    else:
        if selectFlight(flightID):
            print("Sorry! That flight already exists.")
        else:
            flightName = input("Enter name of flight: ")
            maxSeats = input("Enter the max seats for this flight: ")
            if not dc.is_positive_int(maxSeats):
                print("Invalid Number of Seats")
            else:
                seats = input("Enter the initial number of seats for this flight: ")
                if seats > maxSeats:
                    print("Over max seats! Please enter less amount")
                else:
                    flight_op.add_flight(flightID, flightName, maxSeats, seats)
                    print(f"Successfully added a new Flight: ID = #{flightID}, Name = {flightName}!")


def removeFlight():
    flightID = input("Enter the flight ID: ")
    if selectFlight(flightID):
        flight_op.remove_flight(flightID)
        print(f"Successfully removed Flight #{flightID}!")
    else:
        print("Flight not found.")


def addSeats(Flight):
    seats = input("How many seats do you want to add? ")
    if dc.is_positive_int(seats):
        seats = int(seats)
        allocated_seats = Flight['availableseats'] + len(Flight['bookedseats'])
        if allocated_seats+seats <= Flight['maxseats']:
            flight_op.update_flight(Flight['id'], 'availableseats', Flight['availableseats']+seats)
            print(f"Added {seats} seats successfully!")
        else:
            print(f"Sorry! The maximum amount of seats for this flight is {Flight['maxseats']}")
    else:
        print("Invalid Number of Seats")


def removeSeats(Flight):
    seats = input("How many seats do you want to remove? ")
    if dc.is_positive_int(seats):
        seats = int(seats)
        remaining_seats = Flight['availableseats'] - seats
        if remaining_seats >= 0:
            flight_op.update_flight(Flight['id'], 'availableseats', Flight['availableseats']-seats)
            print(f"Removed {seats} seats successfully!")
        elif remaining_seats < 0:
            print(f"Sorry! No seats can be removed")
        elif seats > Flight['availableseats']:
            print(f"Sorry! The maximum amount of seats that can be removed is {Flight['availableseats']}")
    else:
        print("Invalid Number of Seats")


def viewSeats(Flight):
    print(f"Max seats: {Flight['maxseats']}")
    print(f"Available seats: {Flight['availableseats']}")
    print(f"Booked seats: {Flight['bookedseats']}")


def resetFlight(Flight):
    flight_op.update_flight(Flight['id'], 'availableseats', 0)
    flight_op.update_flight(Flight['id'], 'bookedseats', json.dumps([]))
    print(f"Successfully resetted Flight #{Flight['id']}!")


def updateSeats():
    flightID = input("Enter the flight ID: ")
    flight = selectFlight(flightID)
    if flight:
        while True:
            print("\nMODIFY FLIGHT MENU:")
            print("Add seats (A)")
            print("Remove seats (R)")
            print("View max and available seats (V)")
            print("Reset flight (X)")
            print("Exit (Q)")
            pf = input("Enter Your Option: ").lower().replace(" ","")

            match (pf):
                case 'a':
                    addSeats(flight)
                case 'r':
                    removeSeats(flight)
                case 'v':
                    viewSeats(flight)
                case 'x':
                    resetFlight(flight)
                case 'q':
                    break
                case _:
                    print("Oops! Invalid Option!")
            flight_op.update(flight)

    else:
        print("Flight not found.")


def main():
    while True:
        print("\nADMIN CONSOLE:")
        print("Add a flight (A)")
        print("Remove a flight (R)")
        print("Update available seats (U)")
        print("Exit (Q)")
        pf = input("Enter Your Option: ").lower().replace(" ","")

        match (pf):
            case 'a':
                addFlight()
            case 'r':
                removeFlight()
            case 'u':
                updateSeats()
            case 'q':
                db.close()
                break
            case _:
                print("Oops! Invalid Option!")


if __name__ == "__main__":
    main()




