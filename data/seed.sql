PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- =========================
-- parking (1 row)
-- =========================
INSERT INTO parking (name, code, status, created_at, updated_at)
VALUES (
    'Central Parking',
    'PARK-001',
    'active',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- =========================
-- parking_info (linked to parking id=1)
-- NOTE: relies on first parking getting id=1 in a fresh DB
-- =========================
INSERT INTO parking_info (
    parking_id,
    address,
    total_capacity,
    vehicle_capacity,
    motorcycle_capacity,
    open_time,
    close_time,
    supports_24h,
    contact_number,
    description
) VALUES (
    1,
    'Main Street, District 1',
    20,
    15,
    5,
    '06:00',
    '23:00',
    0,
    '02100000000',
    'Initial seeded parking info'
);

-- =========================
-- parking_spot (20 spots: 15 car, 5 motorcycle)
-- status must be: available|occupied|reserved|out_of_service
-- spot_type must be: car|motorcycle|disabled|vip
-- =========================
INSERT INTO parking_spot (
    parking_id, spot_number, spot_type, status, level_label, section_label, is_active
) VALUES
    (1, 'A01', 'car',        'available', 'L1', 'A', 1),
    (1, 'A02', 'car',        'available', 'L1', 'A', 1),
    (1, 'A03', 'car',        'available', 'L1', 'A', 1),
    (1, 'A04', 'car',        'available', 'L1', 'A', 1),
    (1, 'A05', 'car',        'available', 'L1', 'A', 1),
    (1, 'A06', 'car',        'available', 'L1', 'A', 1),
    (1, 'A07', 'car',        'available', 'L1', 'A', 1),
    (1, 'A08', 'car',        'available', 'L1', 'A', 1),
    (1, 'A09', 'car',        'available', 'L1', 'A', 1),
    (1, 'A10', 'car',        'available', 'L1', 'A', 1),
    (1, 'B01', 'car',        'available', 'L1', 'B', 1),
    (1, 'B02', 'car',        'available', 'L1', 'B', 1),
    (1, 'B03', 'car',        'available', 'L1', 'B', 1),
    (1, 'B04', 'car',        'available', 'L1', 'B', 1),
    (1, 'B05', 'car',        'available', 'L1', 'B', 1),
    (1, 'M01', 'motorcycle', 'available', 'L1', 'M', 1),
    (1, 'M02', 'motorcycle', 'available', 'L1', 'M', 1),
    (1, 'M03', 'motorcycle', 'available', 'L1', 'M', 1),
    (1, 'M04', 'motorcycle', 'available', 'L1', 'M', 1),
    (1, 'M05', 'motorcycle', 'available', 'L1', 'M', 1);

-- =========================
-- user (admin + operator)
-- password_hash is placeholder. replace with your real hash strategy later.
-- role must be: admin|operator
-- =========================
INSERT INTO user (full_name, username, password_hash, role, is_active, created_at, updated_at)
VALUES
    ('System Admin', 'admin',    'admin123', 'admin',    1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Main Operator','operator', 'CHANGE_ME_HASH', 'operator', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =========================
-- tariff (active tariffs)
-- tariff_type: hourly|daily|fixed_entry
-- amounts: use base_amount + (hourly_amount/daily_amount/fixed_amount) depending on type
-- =========================
INSERT INTO tariff (
    vehicle_type,
    tariff_type,
    base_amount,
    hourly_amount,
    daily_amount,
    fixed_amount,
    is_active,
    effective_from,
    effective_to,
    description
) VALUES
    ('car',        'hourly',      0, 50000, NULL, NULL, 1, CURRENT_TIMESTAMP, NULL, 'Car hourly tariff'),
    ('motorcycle', 'hourly',      0, 30000, NULL, NULL, 1, CURRENT_TIMESTAMP, NULL, 'Motorcycle hourly tariff'),
    ('car',        'daily',       0, NULL, 300000, NULL, 1, CURRENT_TIMESTAMP, NULL, 'Car daily tariff'),
    ('motorcycle', 'daily',       0, NULL, 180000, NULL, 1, CURRENT_TIMESTAMP, NULL, 'Motorcycle daily tariff'),
    ('car',        'fixed_entry', 0, NULL, NULL, 20000, 1, CURRENT_TIMESTAMP, NULL, 'Car fixed entry fee');

COMMIT;
