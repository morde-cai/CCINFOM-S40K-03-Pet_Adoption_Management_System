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
(1, 'Chloe', (16,3), 'in-shelter', 5, 'male', 2023-06-03, 4.0, '2025-07-06', 'Playful kitten, good with other pets.');
