class ParkingCLI:

    def __init__(
        self,
        register_entry_use_case,
        register_exit_use_case,
        issue_receipt_use_case,
        reports_use_case,
        active_vehicles_use_case,
        manage_users_use_case,
        manage_tariffs_use_case,
    ):
        self.register_entry = register_entry_use_case
        self.register_exit = register_exit_use_case
        self.issue_receipt = issue_receipt_use_case
        self.reports = reports_use_case
        self.active_vehicles = active_vehicles_use_case
        self.manage_users = manage_users_use_case
        self.manage_tariffs = manage_tariffs_use_case

    def run(self):

        while True:

            print("\n===== Parking Management =====")
            print("1. Dashboard")
            print("2. Register Entry")
            print("3. Register Exit")
            print("4. Active Vehicles")
            print("5. Admin Panel")
            print("0. Exit")

            choice = input("Select: ")

            try:

                if choice == "1":
                    self.dashboard()

                elif choice == "2":
                    self.vehicle_entry()

                elif choice == "3":
                    self.vehicle_exit()

                elif choice == "4":
                    self.show_active_vehicles()

                elif choice == "5":
                    self.admin_panel()

                elif choice == "0":
                    print("Goodbye")
                    break

                else:
                    print("Invalid choice")

            except Exception as e:
                print(f"Error: {e}")

    def dashboard(self):

        report = self.reports.full_report()

        print("\n===== DASHBOARD =====")

        print(
            f"Total Spots: "
            f"{report['parking']['total_spots']}"
        )

        print(
            f"Available Spots: "
            f"{report['parking']['available_spots']}"
        )

        print(
            f"Occupied Spots: "
            f"{report['parking']['occupied_spots']}"
        )

        print(
            f"Revenue: "
            f"{report['revenue']['total_revenue']}"
        )

    def vehicle_entry(self):

        print("\n===== VEHICLE ENTRY =====")

        plate = input("Plate Number: ")

        vehicle_type = input(
            "Vehicle Type (car/motorcycle): "
        )

        shift_id = int(
            input("Shift ID: ")
        )

        session = (
            self.register_entry.execute(
                plate_number=plate,
                vehicle_type=vehicle_type,
                shift_id=shift_id,
            )
        )

        print(
            f"Vehicle entered successfully."
        )

        print(
            f"Session ID: {session.id}"
        )

        print(
            f"Spot ID: {session.spot_id}"
        )

    def vehicle_exit(self):

        print("\n===== VEHICLE EXIT =====")

        plate = input(
            "Plate Number: "
        )

        fee = (
            self.register_exit.execute(
                plate
            )
        )

        print(
            f"Calculated Fee: {fee}"
        )

        session_id = int(
            input(
                "Session ID For Receipt: "
            )
        )

        payment_method = input(
            "Payment Method "
            "(cash/card/online): "
        )

        receipt = (
            self.issue_receipt.execute(
                session_id=session_id,
                payment_method=payment_method,
            )
        )

        print(
            "\nReceipt Generated"
        )

        print(
            receipt.format_for_print()
        )

    def show_active_vehicles(self):

        print(
            "\n===== ACTIVE VEHICLES ====="
        )

        vehicles = (
            self.active_vehicles.execute()
        )

        if not vehicles:

            print(
                "No active vehicles."
            )

            return

        for vehicle in vehicles:

            print(
                f"{vehicle['plate_number']} | "
                f"{vehicle['vehicle_type']} | "
                f"Spot {vehicle['spot_id']}"
            )

    def admin_panel(self):

        while True:

            print("\n===== ADMIN =====")
            print("1. Users")
            print("2. Tariffs")
            print("0. Back")

            choice = input(
                "Select: "
            )

            if choice == "1":

                users = (
                    self.manage_users
                    .list_users()
                )

                for user in users:

                    print(
                        user.id,
                        user.username,
                        user.role,
                    )

            elif choice == "2":

                car_tariff = (
                    self.manage_tariffs
                    .get_tariff("car")
                )

                motorcycle_tariff = (
                    self.manage_tariffs
                    .get_tariff(
                        "motorcycle"
                    )
                )

                print(
                    "\nCar Tariff:"
                )
                print(car_tariff)

                print(
                    "\nMotorcycle Tariff:"
                )
                print(
                    motorcycle_tariff
                )

            elif choice == "0":
                return