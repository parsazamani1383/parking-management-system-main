# Public Parking Management System 

**Course Project — Software Engineering**  
**Team Members:** Raef Zandkarimi, Parsa Zamani

A clean-architecture–oriented Parking Management System for managing public parking operations: vehicle entry/exit, parking sessions, spot availability, tariffs, receipts/payments, and reporting — implemented with **Python** and **SQLite**.


---

## Overview

This project focuses on building a maintainable and extensible system using **Clean Architecture** principles:

- **Domain** contains core entities and rules with *no dependency* on infrastructure details.
- **Application** defines use cases and repository interfaces.
- **Infrastructure** provides SQLite implementations (DB connection, repositories, schema init).
- **Interfaces** is reserved for external adapters (CLI now, UI later).

> UI is intentionally postponed. Current focus is the **database + business logic**.

---


## Key Features

### Core Operations
- Register **vehicle entry** (start a parking session)
- Register **vehicle exit** (end session + calculate fee)
- Manage **parking spots** status (free/occupied/reserved/out_of_service)
- Manage **tariffs** (e.g., hourly pricing by vehicle type)
- Issue **receipts** and store payment info

### Reports (via queries/views)
- Active vehicles currently inside the parking
- Session history with full details
- Receipt/payment details
- Parking spot status overview

---

## Tech Stack
- **Python:** 3.10+ recommended (works with 3.8+)
- **Database:** SQLite 3
- **DB Driver:** `sqlite3` (Python standard library)
- **Architecture:** Clean Architecture + Clean Code conventions
- **UI:** Not implemented yet (planned later)


---

## Project Structure (Clean Architecture)
```bash 
parking-management-system/
├── README.md
├── .gitignore
├── requirements.txt
├── run.py
├── data/
│   ├── parking.db          (SQLite Database File)
│   ├── schema.sql          (Database Tables Definition)
│   └── seed.sql            (Initial Sample Data)
├── docs/
│   ├── database-design.pdf
│   ├── erd.png
│   └── class-diagram.png
└── src/
    ├── config/
    │   └── settings.py     (System Configurations)
    ├── domain/
    │   ├── __init__.py
    │   ├── entities/       (Core Business Models)
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── vehicle.py
    │   │   ├── parking_spot.py
    │   │   ├── parking_session.py
    │   │   ├── tariff.py
    │   │   ├── receipt.py
    │   │   ├── operator_shift.py
    │   │   └── parking_info.py
    │   └── exceptions.py   (Domain Specific Errors)
    ├── application/
    │   ├── __init__.py
    │   ├── interfaces/     (Repository Abstracts)
    │   │   ├── user_repo.py
    │   │   ├── vehicle_repo.py
    │   │   ├── spot_repo.py
    │   │   ├── session_repo.py
    │   │   └── tariff_repo.py
    │   ├── services/       (Business Logic Services)
    │   │   └── fee_calculator.py
    │   └── use_cases/      (Application Workflows)
    │       ├── register_entry.py
    │       ├── register_exit.py
    │       ├── issue_receipt.py
    │       └── reports.py
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── db/
    │   │   ├── connection.py
    │   │   └── migrations.py
    │   └── repositories/   (Data Access Implementation)
    │       ├── user_repo_sqlite.py
    │       ├── vehicle_repo_sqlite.py
    │       ├── spot_repo_sqlite.py
    │       ├── session_repo_sqlite.py
    │       └── tariff_repo_sqlite.py
    └── ui/                 (User Interface Layer)
        └── cli/
            └── app.py

```


---


### Dependency Rule (Important)
Dependencies must point inward:
- `domain` depends on nothing
- `application` depends on `domain`
- `infrastructure` depends on `application` (implements interfaces)
- `interfaces` calls `application` use cases

---

## Database Design

### Main Tables
- `User` (roles: admin/operator/owner)
- `Parking`
- `ParkingSpot` (status: free/occupied/reserved/out_of_service)
- `Vehicle`
- `Tariff`
- `ParkingSession` (status: active/closed)
- `Receipt`

### Constraints / Integrity
- Primary keys with `AUTOINCREMENT`
- Foreign keys with `FOREIGN KEY` (enabled using `PRAGMA foreign_keys = ON;`)
- `CHECK` constraints for enumerated fields (role, status, ...)

### Indexes & Views
Schema also includes (or will include):
- **Indexes** for frequently searched fields (e.g., plate number, session status)
- **Views** for reporting, such as:
  - Active vehicles
  - Session details
  - Receipt details
  - Spot status view

> Database scripts:
- `data/schema.sql` (full schema)
- `data/seed.sql` (optional sample data)

---

## Setup & Run

### 1) Create Virtual Environment
```bash
python -m venv .venv
