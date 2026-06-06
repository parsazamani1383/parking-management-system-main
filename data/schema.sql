PRAGMA foreign_keys = ON;

-- =========================
-- Table: parking
-- =========================
CREATE TABLE IF NOT EXISTS parking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('active', 'inactive', 'maintenance')),
    created_at TEXT NOT NULL,
    updated_at TEXT
);

-- =========================
-- Table: parking_info
-- =========================
CREATE TABLE IF NOT EXISTS parking_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL UNIQUE,
    address TEXT NOT NULL,
    total_capacity INTEGER NOT NULL CHECK (total_capacity >= 0),
    vehicle_capacity INTEGER NOT NULL CHECK (vehicle_capacity >= 0),
    motorcycle_capacity INTEGER NOT NULL CHECK (motorcycle_capacity >= 0),
    open_time TEXT,
    close_time TEXT,
    supports_24h INTEGER NOT NULL DEFAULT 0 CHECK (supports_24h IN (0, 1)),
    contact_number TEXT,
    description TEXT,
    FOREIGN KEY (parking_id) REFERENCES parking(id) ON DELETE CASCADE
);

-- =========================
-- Table: user
-- =========================
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'operator')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT
);

-- =========================
-- Table: parking_spot
-- =========================
CREATE TABLE IF NOT EXISTS parking_spot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL,
    spot_number TEXT NOT NULL,
    spot_type TEXT NOT NULL CHECK (spot_type IN ('car', 'motorcycle', 'disabled', 'vip')),
    status TEXT NOT NULL CHECK (status IN ('available', 'occupied', 'reserved', 'out_of_service')),
    level_label TEXT,
    section_label TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (parking_id) REFERENCES parking(id) ON DELETE CASCADE,
    UNIQUE (parking_id, spot_number)
);

-- =========================
-- Table: vehicle
-- =========================
CREATE TABLE IF NOT EXISTS vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL CHECK (vehicle_type IN ('car', 'motorcycle')),
    color TEXT,
    brand TEXT,
    model TEXT,
    owner_name TEXT,
    owner_phone TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

-- =========================
-- Table: tariff
-- =========================
CREATE TABLE IF NOT EXISTS tariff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT NOT NULL CHECK (vehicle_type IN ('car', 'motorcycle')),
    tariff_type TEXT NOT NULL CHECK (tariff_type IN ('hourly', 'daily', 'fixed_entry')),
    base_amount REAL NOT NULL CHECK (base_amount >= 0),
    hourly_amount REAL CHECK (hourly_amount >= 0),
    daily_amount REAL CHECK (daily_amount >= 0),
    fixed_amount REAL CHECK (fixed_amount >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    description TEXT
);

-- =========================
-- Table: operator_shift
-- =========================
CREATE TABLE IF NOT EXISTS operator_shift (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    parking_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    shift_status TEXT NOT NULL CHECK (shift_status IN ('open', 'closed')),
    opening_note TEXT,
    closing_note TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE RESTRICT,
    FOREIGN KEY (parking_id) REFERENCES parking(id) ON DELETE CASCADE
);

-- =========================
-- Table: parking_session
-- =========================
CREATE TABLE IF NOT EXISTS parking_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    parking_spot_id INTEGER,
    opened_by_user_id INTEGER NOT NULL,
    closed_by_user_id INTEGER,
    tariff_id INTEGER,
    entry_time TEXT NOT NULL,
    exit_time TEXT,
    session_status TEXT NOT NULL CHECK (session_status IN ('active', 'completed', 'cancelled')),
    calculated_amount REAL NOT NULL DEFAULT 0 CHECK (calculated_amount >= 0),
    paid_amount REAL NOT NULL DEFAULT 0 CHECK (paid_amount >= 0),
    note TEXT,
    FOREIGN KEY (parking_id) REFERENCES parking(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id) ON DELETE RESTRICT,
    FOREIGN KEY (parking_spot_id) REFERENCES parking_spot(id) ON DELETE SET NULL,
    FOREIGN KEY (opened_by_user_id) REFERENCES user(id) ON DELETE RESTRICT,
    FOREIGN KEY (closed_by_user_id) REFERENCES user(id) ON DELETE RESTRICT,
    FOREIGN KEY (tariff_id) REFERENCES tariff(id) ON DELETE SET NULL
);

-- =========================
-- Table: receipt
-- =========================
CREATE TABLE IF NOT EXISTS receipt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_session_id INTEGER NOT NULL UNIQUE,
    receipt_number TEXT NOT NULL UNIQUE,
    issued_by_user_id INTEGER NOT NULL,
    issued_at TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'card', 'online')),
    payment_status TEXT NOT NULL CHECK (payment_status IN ('paid', 'unpaid', 'refunded')),
    description TEXT,
    FOREIGN KEY (parking_session_id) REFERENCES parking_session(id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by_user_id) REFERENCES user(id) ON DELETE RESTRICT
);

-- =========================
-- Indexes
-- =========================
CREATE INDEX IF NOT EXISTS idx_user_username ON user(username);
CREATE INDEX IF NOT EXISTS idx_vehicle_plate_number ON vehicle(plate_number);
CREATE INDEX IF NOT EXISTS idx_parking_spot_parking_id ON parking_spot(parking_id);
CREATE INDEX IF NOT EXISTS idx_parking_session_vehicle_id ON parking_session(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_parking_session_parking_id ON parking_session(parking_id);
CREATE INDEX IF NOT EXISTS idx_parking_session_status ON parking_session(session_status);
CREATE INDEX IF NOT EXISTS idx_operator_shift_user_id ON operator_shift(user_id);
CREATE INDEX IF NOT EXISTS idx_operator_shift_parking_id ON operator_shift(parking_id);
CREATE INDEX IF NOT EXISTS idx_receipt_receipt_number ON receipt(receipt_number);
CREATE INDEX IF NOT EXISTS idx_tariff_vehicle_type_active ON tariff(vehicle_type, is_active);
