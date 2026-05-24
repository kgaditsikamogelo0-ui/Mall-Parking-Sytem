from datetime import datetime
import math


# =========================
# SECTION 1 — MALL CLASSES
# =========================

class Mall:

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.current_vehicles = 0

    def calculate_fee(self, hours):
        return 0


# Vaal Mall
class VaalMall(Mall):

    def calculate_fee(self, hours):

        # Flat Rate
        return 15


# River Square
class RiverSquare(Mall):

    def calculate_fee(self, hours):

        # R10 per hour
        return math.ceil(hours) * 10


# Evaton Mall
class EvatonMall(Mall):

    def calculate_fee(self, hours):

        fee = math.ceil(hours) * 12

        # Daily Cap
        if fee > 60:
            fee = 60

        return fee


# =========================
# SECTION 2 — CREATE MALLS
# =========================

vaal = VaalMall("Vaal Mall", 250)

riversquare = RiverSquare("River Square Shopping Center", 180)

evaton = EvatonMall("Evaton Mall", 150)


# =========================
# SECTION 3 — REGISTER
# =========================

def register():

    print("\n=== REGISTER ===")

    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (customer/admin/owner): ")

    file = open("users.txt", "a")

    file.write(username + "," + password + "," + role + "\n")

    file.close()

    print("Registration successful")


# =========================
# SECTION 4 — LOGIN
# =========================

def login():

    print("\n=== LOGIN ===")

    username = input("Enter username: ")
    password = input("Enter password: ")

    file = open("users.txt", "r")

    for line in file:

        data = line.strip().split(",")

        saved_username = data[0]
        saved_password = data[1]
        role = data[2]

        if username == saved_username and password == saved_password:

            print("Login successful")

            file.close()

            return username, role

    file.close()

    print("Invalid login")

    return None, None


# =========================
# SECTION 5 — SELECT MALL
# =========================

def select_mall():

    print("\n=== SELECT MALL ===")

    print("1. Vaal Mall")
    print("2. River Square Shopping Centre")
    print("3. Evaton  Mall")

    choice = input("Enter choice: ")

    if choice == "1":
        return vaal

    elif choice == "2":
        return riversquare

    elif choice == "3":
        return evaton

    else:
        print("Invalid choice")
        return None


# =========================
# SECTION 6 — VEHICLE ENTRY
# =========================

def vehicle_entry(username, mall):

    print("\n=== VEHICLE ENTRY ===")

    if mall.current_vehicles >= mall.capacity:

        print("Parking is full")
        return

    car_number = input("Enter vehicle registration: ")

    entry_time = datetime.now()

    file = open("parking.txt", "a")

    file.write(
        username + "," +
        car_number + "," +
        mall.name + "," +
        str(entry_time) + ",IN\n"
    )

    file.close()

    mall.current_vehicles += 1

    print("Vehicle entered successfully")


# =========================
# SECTION 7 — VEHICLE EXIT
# =========================

def vehicle_exit(username, mall):

    print("\n=== VEHICLE EXIT ===")

    car_number = input("Enter vehicle registration: ")

    file = open("parking.txt", "r")

    lines = file.readlines()

    file.close()

    found = False

    for line in lines:

        data = line.strip().split(",")

        saved_user = data[0]
        saved_car = data[1]
        saved_mall = data[2]
        entry_time = data[3]
        status = data[4]

        if saved_user == username and saved_car == car_number and status == "IN":

            found = True

            entry = datetime.fromisoformat(entry_time)

            exit_time = datetime.now()

            duration = exit_time - entry

            hours = duration.total_seconds() / 3600

            fee = mall.calculate_fee(hours)

            print("Hours Parked:", round(hours, 2))

            if mall.name == "Vaal Mall":
                print("Pricing Type: Flat Rate")

            elif mall.name == "River Square Shopping Centre":
                print("Pricing Type: Hourly Rate")

            else:
                print("Pricing Type: Hourly Rate With Daily Cap")

            print("Parking Fee: R", fee)

            pay = input("Make payment? (yes/no): ")

            if pay == "yes":

                payment_file = open("payments.txt", "a")

                payment_file.write(
                    username + "," +
                    mall.name + "," +
                    str(fee) + "\n"
                )

                payment_file.close()

                mall.current_vehicles -= 1

                print("Payment successful")

            else:
                print("Payment cancelled")

    if found == False:
        print("Vehicle not found")


# =========================
# SECTION 8 — PARKING HISTORY
# =========================

def view_parking_history(username):

    print("\n=== PARKING HISTORY ===")

    file = open("parking.txt", "r")

    for line in file:

        data = line.strip().split(",")

        if data[0] == username:
            print(line)

    file.close()


# =========================
# SECTION 9 — PAYMENT HISTORY
# =========================

def view_payment_history(username):

    print("\n=== PAYMENT HISTORY ===")

    file = open("payments.txt", "r")

    for line in file:

        data = line.strip().split(",")

        if data[0] == username:
            print(line)

    file.close()


# =========================
# SECTION 10 — CURRENT VEHICLES
# =========================

def view_current_vehicles():

    print("\n=== CURRENT VEHICLES ===")

    file = open("parking.txt", "r")

    for line in file:

        data = line.strip().split(",")

        status = data[4]

        if status == "IN":
            print(line)

    file.close()


# =========================
# SECTION 11 — REPORTS
# =========================

def reports():

    print("\n=== REPORTS ===")

    total_revenue = 0
    total_vehicles = 0

    file = open("payments.txt", "r")

    for line in file:

        data = line.strip().split(",")

        total_revenue += float(data[2])

        total_vehicles += 1

    file.close()

    print("Total Vehicles:", total_vehicles)

    print("Total Revenue: R", total_revenue)


# =========================
# SECTION 12 — CUSTOMER MENU
# =========================

def customer_menu(username):

    mall = select_mall()

    if mall == None:
        return

    while True:

        print("\n=== CUSTOMER MENU ===")

        print("1. Vehicle Entry")
        print("2. Vehicle Exit")
        print("3. View Parking History")
        print("4. View Payment History")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            vehicle_entry(username, mall)

        elif choice == "2":
            vehicle_exit(username, mall)

        elif choice == "3":
            view_parking_history(username)

        elif choice == "4":
            view_payment_history(username)

        elif choice == "5":
            break

        else:
            print("Invalid choice")


# =========================
# SECTION 13 — ADMIN MENU
# =========================

def admin_menu():

    while True:

        print("\n=== ADMIN MENU ===")

        print("1. View Current Vehicles")
        print("2. View Reports")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_current_vehicles()

        elif choice == "2":
            reports()

        elif choice == "3":
            break

        else:
            print("Invalid choice")


# =========================
# SECTION 14 — OWNER MENU
# =========================

def owner_menu():

    while True:

        print("\n=== OWNER MENU ===")

        print("1. View Reports")
        print("2. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            reports()

        elif choice == "2":
            break

        else:
            print("Invalid choice")


# =========================
# SECTION 15 — MAIN PROGRAM
# =========================

while True:

    print("\n===================================")
    print("VAAL SMART MALL PARKING SYSTEM")
    print("===================================")

    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        register()

    elif choice == "2":

        username, role = login()

        if username != None:

            if role == "customer":
                customer_menu(username)

            elif role == "admin":
                admin_menu()

            elif role == "owner":
                owner_menu()

            else:
                print("Invalid role")

    elif choice == "3":

        print("System closed")

        break

    else:
        print("Invalid choice")
