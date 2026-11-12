-- mysql -u <user> -p <database> < seed_data.sql




USE pet_adoption_db

-- Clear existing data (safe to run multiple times during dev)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE pet_adoption_shelter;
TRUNCATE TABLE pet_adoption_species;
TRUNCATE TABLE pet_adoption_breed;
TRUNCATE TABLE pet_adoption_pet;
TRUNCATE TABLE pet_adoption_staffrole;
TRUNCATE TABLE pet_adoption_staff;
TRUNCATE TABLE pet_adoption_adopter;
TRUNCATE TABLE pet_adoption_adoption;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- shelters
-- ============================================================
INSERT INTO pet_adoption_shelter (id, shelter_name, address, capacity) VALUES 
(1, 'Paws - PH', 'Manila', 10),
(2, 'Paws - CN', 'Shanghai', 40),
(3, 'Paws - JP', 'Hokkaido', 30),
(4, 'Paws - US', 'New York', 50),
(5, 'Paws - SG', 'Singapore', 20);

-- ============================================================
-- species
-- ============================================================
INSERT INTO pet_adoption_species (id, name) VALUES 
(1, 'Dog'),
(2, 'Cat'),
(3, 'Rabbit');

-- ============================================================
-- breeds
-- ============================================================
INSERT INTO pet_adoption_breed (id, name, species_id) VALUES 
(1, 'Aspin', 1),
(2, 'Chihuahua', 1),
(3, 'Poodle', 1),
(4, 'Puspin', 2),
(5, 'British Shorthair', 2),
(6, 'Persian', 2),
(7, 'Mini Rex', 3),
(8, 'Flemish Giant', 3),
(9, 'Netherland Dwarf', 3);

-- ============================================================
-- pets
-- ============================================================
INSERT INTO pet_adoption_pet (id, name, breed_id, status, shelter_id, sex, date_of_birth, kg_weight, intake_date, description) VALUES
(1, 'Chloe', 3, 'in-shelter', 5, 'male', 2023-06-03, 4.0, '2025-07-06', 'Playful kitten, good with other pets.');


-- ============================================================
-- staffroles
-- ============================================================
INSERT INTO pet_adoption_staffrole (id, role_name) VALUES
(1, 'Manager'),
(2, 'Veterinarian'),
(3, 'Counselor'),
(4, 'Volunteer Coordinator'),
(5, 'Assistant');

-- ============================================================
-- staffs
-- ============================================================
INSERT INTO pet_adoption_staff (id, first_name, last_name, date_of_birth, sex, email, contact_number, address, role_id, status, shelter_id, hire_date) VALUES
(1, 'Maria', 'Santos', '1985-03-14', 'female', 'maria.santos@pawshaven.ph', '09171234501', '12 Rizal St, Quezon City', 1, 'active', 1, '2019-06-01');


-- ============================================================
-- adopters
-- ============================================================
INSERT INTO pet_adoption_adopter (id, first_name, last_name, date_of_birth, sex, email, contact_number, address) VALUES
(1, 'Ricardo', 'Garcia', '1995-06-03', 'male', 'ricardogarcia1@gmail.com', '09181590830', '89 Quezon Ave, Pasig');

-- ============================================================
-- adoptions
-- ============================================================
INSERT INTO pet_adoption_adoption (id, pet_id, adopter_id, staff_id, fee, request_date, adoption_date, status) VALUES
(1, 1, 11, 1, 500.0, '2026-05-04', '2026-05-04', 'completed') -- same-day turnaround,