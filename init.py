import main as fbs
from database import Database
import sql_op.flight_op as flight_op

db = Database("FlightBookingSystem")


def start(): 
	flights = flight_op.get_flights()

	if not flights:
		print("No flights added yet!")
		exit()

	while True:	 
		print("\nWelcome!\n\nPlease Choose A Flight:")
		for flight in flights:
			print(f"{flight['name'].capitalize()} ({flight['id']})")

		flightid = input("\nEnter Your Flight Id, or Press (Q) to Exit: ").lower().strip()

		if flightid in [flight['id'] for flight in flights]:
			selected_flight = flight_op.select_flight(flightid)
			fbs.main(selected_flight)

		elif flightid=='q':
			print("Goodbye!")
			db.close()
			break

		else:
			print("Oops! Invalid Option")


if __name__ == '__main__':
	start()
