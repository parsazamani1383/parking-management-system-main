# Public Parking Management System

**Software Engineering Course Project**

**Team Members:** Raef Zandkarimi, Parsa Zamani

A desktop-based Parking Management System developed with **Python** and **SQLite** for managing parking operations, including vehicle entry and exit, parking spots, tariffs, users, parking sessions, payments, receipts, and reports.

The project is designed using **Clean Architecture** principles to keep the business logic independent from infrastructure and user-interface concerns.

---

## Overview

The Parking Management System provides a complete workflow for operating a public parking facility.

The system supports different user roles and provides dedicated functionality for parking operators and administrators. Operators can register vehicle entries and exits, manage active parking sessions, calculate parking fees, and issue receipts. Administrators can manage users, parking spots, tariffs, and access management features through the desktop interface.

The project is organized into separate layers for **Domain**, **Application**, **Infrastructure**, and **UI**, making the system easier to maintain, test, and extend.

---

## Features

### Authentication

* User login and authentication
* Role-based access for administrators and operators
* User management

### Vehicle Management

* Register vehicle entry
* Register vehicle exit
* Track active vehicles inside the parking
* Support for different vehicle types
* License plate conversion and handling

### Parking Spot Management

* Create parking spots
* Update parking spot information
* Delete parking spots
* Enable or disable parking spots
* Track parking spot availability and status

### Tariff Management

* Manage parking tariffs
* Update tariff information
* Calculate parking fees based on the configured tariff

### Parking Sessions

* Create and manage parking sessions
* Track entry and exit times
* Associate vehicles with parking spots
* Calculate the final parking amount
* Record payment information

### Receipts & Payments

* Issue parking receipts
* Store payment information
* Generate receipt PDFs

### Dashboard & Reports

* Dashboard for monitoring parking operations
* View active vehicles
* Access parking and session information
* Generate and display operational reports

### Desktop User Interface

The project includes a desktop graphical user interface with dedicated windows for:

* Login
* Dashboard
* Vehicle Entry
* Vehicle Exit & Payment
* Active Vehicles
* Administration Panel
* User Management
* Parking Spot Management

---

## Architecture

The project follows a **Clean Architecture–oriented structure**.

### Domain

Contains the core business entities and domain-specific exceptions.

The domain layer is independent of the database and user interface.

### Application

Contains application-level business logic, repository interfaces, services, and use cases.

### Infrastructure

Contains the concrete implementations required to communicate with external systems, including the SQLite database and repository implementations.

### UI

Contains the user interfaces of the application, including both the desktop interface and CLI interface.

### Utils

Contains supporting utilities such as license plate conversion and receipt PDF generation.

---

## Project Structure

```text
parking-management-system/
├── README.md
├── .gitignore
├── requirements.txt
├── run.py
│
├── data/
│   ├── parking.db
│   ├── schema.sql
│   └── seed.sql
│
├── docs/
│   ├── .gitkeep
│   ├── DB_implementation_HW05_Parsa_Raef.pdf
│   ├── Parking_Management_User_Forms_and_Flow_Raef_Parsa.pdf
│   ├── SE_ClassDiagram.svg
│   └── SE_Use-Case.svg
│
├── src/
│   ├── application/
│   │   ├── interfaces/
│   │   ├── services/
│   │   └── use_cases/
│   │
│   ├── config/
│   │
│   ├── domain/
│   │   ├── entities/
│   │   └── exceptions.py
│   │
│   ├── infrastructure/
│   │   ├── db/
│   │   └── repositories/
│   │
│   ├── ui/
│   │   ├── assets/
│   │   ├── cli/
│   │   └── desktop/
│   │
│   └── utils/
│
└── test/
    ├── test_connection.py
    └── domain/
```

### Application Layer

```text
src/application/
├── interfaces/
│   ├── parking_repo.py
│   ├── receipt_repo.py
│   ├── session_repo.py
│   ├── shift_repo.py
│   ├── spot_repo.py
│   ├── tariff_repo.py
│   ├── user_repo.py
│   └── vehicle_repo.py
│
├── services/
│   ├── auth_service.py
│   └── fee_calculator.py
│
└── use_cases/
    ├── admin_panel_usecase.py
    ├── create_parking_spot_usecase.py
    ├── create_user_usecase.py
    ├── dashboard_usecase.py
    ├── delete_parking_spot_usecase.py
    ├── issue_receipt.py
    ├── list_active_vehicles.py
    ├── manage_tariffs.py
    ├── manage_users.py
    ├── register_entry.py
    ├── register_exit.py
    ├── register_exit_usecase.py
    ├── reports.py
    ├── show_active_vehicles.py
    ├── toggle_parking_spot_usecase.py
    ├── update_parking_spot_usecase.py
    ├── update_tariff_usecase.py
    └── update_user_usecase.py
```

### Domain Layer

```text
src/domain/
├── entities/
│   ├── operator_shift.py
│   ├── parking.py
│   ├── parking_info.py
│   ├── parking_session.py
│   ├── parking_spot.py
│   ├── receipt.py
│   ├── tariff.py
│   ├── user.py
│   └── vehicle.py
│
└── exceptions.py
```

### Infrastructure Layer

```text
src/infrastructure/
├── db/
│   ├── connection.py
│   └── migrations.py
│
└── repositories/
    ├── parking_repo_sqlite.py
    ├── receipt_repo_sqlite.py
    ├── session_repo_sqlite.py
    ├── shift_repo_sqlite.py
    ├── spot_repo_sqlite.py
    ├── tariff_repo_sqlite.py
    ├── user_repo_sqlite.py
    └── vehicle_repo_sqlite.py
```

### User Interface

```text
src/ui/
├── assets/
│   ├── fonts/
│   │   └── BNazanin.ttf
│   ├── logo.png
│   └── logo1.png
│
├── cli/
│   └── app.py
│
└── desktop/
    ├── active_vehicles_window.py
    ├── add_parking_spot_window.py
    ├── add_user_window.py
    ├── admin_panel_window.py
    ├── dashboard_window.py
    ├── login_window.py
    ├── register_entry_window.py
    └── register_exit_window.py
```

---

## Database

The project uses **SQLite** as its database.

The database files are located in the `data/` directory:

```text
data/
├── parking.db
├── schema.sql
└── seed.sql
```

* `parking.db` — SQLite database used by the application
* `schema.sql` — Database schema and table definitions
* `seed.sql` — Initial/sample database data

The database is integrated with the infrastructure layer through the SQLite database connection and repository implementations.

---

## User Interface

The final version of the project includes a desktop graphical interface.

### Login

The login window provides authentication for system users.

<!-- Add screenshot here -->

### Dashboard

The dashboard provides an overview of the current parking system.

<!-- Add screenshot here -->

### Vehicle Entry

Operators can register incoming vehicles and create a new parking session.

<!-- Add screenshot here -->

### Vehicle Exit & Payment

Operators can register vehicle exits, calculate the parking fee, and process the payment.

<!-- Add screenshot here -->

### Active Vehicles

The active vehicles window displays vehicles currently inside the parking.

<!-- Add screenshot here -->

### Administration Panel

Administrators can access management functionality through the administration panel.

<!-- Add screenshot here -->

### Parking Spot Management

Parking spots can be created, updated, deleted, enabled, or disabled through the management interface.

<!-- Add screenshot here -->

### User Management

Administrators can manage system users through the user management interface.

<!-- Add screenshot here -->

---

## Documentation

Additional project documentation is available in the `docs/` directory.

### Class Diagram

`docs/SE_ClassDiagram.svg`

### Use Case Diagram

`docs/SE_Use-Case.svg`

### Database Implementation

`docs/DB_implementation_HW05_Parsa_Raef.pdf`

### User Forms & Flow

`docs/Parking_Management_User_Forms_and_Flow_Raef_Parsa.pdf`

---

## Testing

The project includes tests for database connectivity and core domain entities.

```text
test/
├── test_connection.py
└── domain/
    ├── test_operator_shift.py
    ├── test_parking_session.py
    ├── test_parking_spot.py
    ├── test_receipt.py
    ├── test_tariff.py
    ├── test_user.py
    └── test_vehicle.py
```

---

## Requirements

The project requires:

* Python 3.x
* SQLite 3
* Dependencies listed in `requirements.txt`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/parsazamani1383/parking-management-system-main.git
cd parking-management-system-main
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the main application using:

```bash
python run.py
```

The application will start the parking management system.

---

## Technologies

* **Python**
* **SQLite**
* **Tkinter / Python Desktop UI**
* **Clean Architecture**
* **Object-Oriented Programming**
* **Repository Pattern**
* **Unit Testing**
* **PDF Receipt Generation**

---

## Team

This project was developed as a **Software Engineering course project** by:

* **Raef Zandkarimi**
* **Parsa Zamani**

---

## Repository

GitHub Repository:

https://github.com/parsazamani1383/parking-management-system-main

```
```
