import airportsdata
airports = airportsdata.load("IATA")  # key is ICAO code, the default
import email_operations as eo
import sql_op.flight_op as flight_op
import sql_op.booking_op as booking_op
import datacomp as dc
import json


def date_check(date):
    if date[0:1][0] == "0":
        dd = int(date[1])
    if date[2:3][0] == "0":
        mm = int(date[3])
    if date[4:5][0] == "0":
        return "False"
    
    dd = int(date[0:2])
    mm = int(date[2:4])
    yy = int(date[4:6])

    if dd > 28 and mm == 2:
        return "False"
    elif yy != 24:
        return "notavailable"
    elif dd > 31:
        return "False"
    elif dd == 31 and mm % 2 == 0 and mm != 8:
        return "False"
    elif (dd == 31 and mm % 2 != 0) and (mm == 9 or mm == 11):
        return "False"
    elif mm < 1 or mm > 12:
        return "False"
    else:
        DD = str(dd)
        MM = str(mm)
        YY = str(yy)
        if len(DD) == 1:
            DD = "0" + DD
        if len(MM) == 1:
            MM = "0" + MM
        flight_date = DD + "/" + MM + "/" + YY
        return flight_date


def write_confirmation_statement(
    Flight="", your_seats=[], confirm_date="", origin_code="", destination_code="", passenger_name="", email="", file_path=""
):

    with open(
        file_path,
        "w"
    ) as myfile:
        myfile.write(
            f"""
Dear {passenger_name},


Your {Flight['name']} Flight Has Successfully Been Booked.

Flying On: {confirm_date}

Origin: {airports[origin_code]['name']}, {airports[origin_code]['city']}, {airports[origin_code]['country']}

Destination: {airports[destination_code]['name']}, {airports[destination_code]['city']}, {airports[destination_code]['country']}

Number Of Passengers: {len(your_seats)}

Seat Numbers: {your_seats}


Any queries or information that you are unsure about, Please visit our website or contact us via phone/email.


Thanks,


{Flight['name']}

			"""
        )
    """
    try:
        send_email(file_path, passenger_name, email)
    except Exception as e:
        print("Something went wrong...Please check your details and try again.")
        print(e)
    else:
    """
    flight_op.update_flight(Flight['id'], 'availableseats', Flight['availableseats']-len(your_seats))
    '''
    booking_op.add_booking(
        confirm_date, 
        f"airports[origin_code]['name'] ({origin_code})",
        f"airports[destination_code]['name'] ({destination_code})",
        len(your_seats),
        Flight['id']
    )
    '''
    print("Flight booked")


def send_email(file_path, passenger_name, email):
    with open(file_path, "rb") as myfile:
        file_name = myfile.name
        host_email_address = "avnikumar32@gmail.com"
        host_password = "Stoke0Pesky**unjustly6Designer"
        subject = "Flight Booked Successfully!"
        data = f"Hi {passenger_name}, Please See Attached, Your Flight Booking Details"
        subtype = "txt"
        eo.send_email(
            file_name, email, host_email_address, subject, data, subtype, host_password
        )


def validateAirportCode(orgncode,destcode):
    try:
        airports[orgncode]
    except KeyError:
        pass
    else:
        try:
            airports[destcode]
        except KeyError:
            pass
        else:
            return True
        

def validateDate(date):
    if date < 0:
        print("Invalid Date!")
    else:
        date = str(date)
        if len(date) == 5:
            date = "0" + date
        if len(date) == 6:
            confirm_date = date_check(date)
            if confirm_date == "False":
                print("Invalid Date!")
            elif confirm_date == "notavailable":
                print("Sorry! Only 2024 Flights Are Available!")
            else:
                print("Valid date!")
                return confirm_date
        else:
            print("Date Must be 6 Digits!")


def bookFlight(Flight, passenger_name, seats):
    file_path = f"C:\\Users\\avnik\\Documents\\Python Projects\\Flight Booking System\\Confirmation Statements\\{Flight['name']}{id(passenger_name)}.txt"
    confirm_date = ""
    email = input("\nPlease Enter Your Email Address: ")
    origin_code = input("Enter The Origin Airport Code: ").upper()
    destination_code = input("Enter The Destination Airport Code: ").upper()
    date = input("Enter The Date Of Flight: ")
    if not dc.is_int(date):
        print("Invalid Date!")
    else:
        print()
        date = int(date)
        validAirportCode = validateAirportCode(origin_code, destination_code)
        validDate = validateDate(date)

        if validAirportCode and validDate:
            confirm_date = validDate
            your_seats = appendBookedSeat(Flight, seats)

            write_confirmation_statement(
                Flight=Flight,
                your_seats=your_seats,
                confirm_date=confirm_date,
                origin_code=origin_code,
                destination_code=destination_code,
                passenger_name=passenger_name,
                email=email,
                file_path=file_path
            )

        elif not validAirportCode:
            print("Invalid origin/destination code.")


def appendBookedSeat(Flight,seats):
    your_seats = []
    count = 0
    x = 1
    bookedseats = Flight['bookedseats']
    while count < seats:
        if x in bookedseats:
            x += 1
            continue
        else:
            if len(str(x)) == 1:
                your_seats.append(f"00{x}")
            elif len(str(x)) == 2:
                your_seats.append(f"0{x}")
            else:
                your_seats.append(str(x))

            bookedseats.append(x)
            x += 1
            count += 1

    json_data = json.dumps(bookedseats)
    flight_op.update_flight(Flight['id'], 'bookedseats', json_data)
    return your_seats
