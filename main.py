import book_flight
import sql_op.flight_op as flight_op
import datacomp as dc


def customer(Flight):
    print("\nWelcome! Please Enter Your Name:")
    passenger_name = input()

    seats = input("How many seats do you want to book? ")
    if dc.is_positive_int(seats):
        seats = int(seats)
        status = checkAvailableSeats(Flight,seats)
        if status == True:
            book_flight.bookFlight(
                Flight, passenger_name, seats
            )
    else:
        print("Invalid Number of Seats!")
            

def checkAvailableSeats(Flight,seats):
    if seats < 0:
        print("Invalid Number of Seats!")
    if Flight['availableseats'] == 0 and not Flight['bookedseats']:
        print("Sorry! Seats aren't allocated yet")
    elif Flight['availableseats']==0:
        print("Sorry! Flight is fully booked")
    elif Flight['availableseats'] < seats:
        print(f"Sorry! There are only {Flight['availableseats']} seats available")
    else:
        return True


def displaySeats(Flight):
    if Flight['availableseats'] == 0:
        print("There are currently no seats available")
    elif Flight['availableseats'] == 1:
        print(f"There is 1 seat Available")
    else:
        print(f"There are {Flight['availableseats']} seats available")


def create_admin_pin(Flight):
    print("Please Create A PIN:")
    adminPIN = input()
    if not dc.is_int(adminPIN):
        print("Sorry! PIN can only consist of numbers!")
    else:
        if int(adminPIN) <= 0:
            print("Invalid PIN")
        else:
            if len(adminPIN) != 6:
                print("Sorry! PIN must be 6 Digits")
            else:
                flight_op.update_flight(Flight['id'], 'adminpin', adminPIN)
                print("Successfully created a new admin PIN.")


def main(Flight):

    mainMenuOptions = {
        'c':customer,
        'customer':customer,
        'displayseats':displaySeats,
        'd':displaySeats,
    }

    while True:
        flight_op.update(Flight)
        option = (
            input(
                f"\nWelcome To {Flight['name'].capitalize()}!\nMAIN MENU:\nCustomer (c)\nDisplay Seats (d)\n(Exit) (Q)\nEnter Your Role/Option: "
            )
            .lower()
            .replace(" ", "")
        )
        if option in mainMenuOptions:
            mainMenuOptions[option](Flight)
        elif option == 'q' or option == 'exit':
            break
        else:
            print("Oops! Invalid Role/Option!")

