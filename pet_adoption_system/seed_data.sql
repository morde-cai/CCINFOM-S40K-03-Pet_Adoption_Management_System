-- mysql -u root -p pet_adoption_db < seed_data.sql

USE pet_adoption_db;

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
(1, 'Paws - PH', 'Manila', 5),
(2, 'Paws - CN', 'Shanghai', 20),
(3, 'Paws - JP', 'Hokkaido', 15),
(4, 'Paws - US', 'New York', 25),
(5, 'Paws - SG', 'Singapore', 10);

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
(1, 'Charlie', 3, 'in-shelter', 2, 'male', '2025-03-17', 19.0, '2026-01-18', 'Friendly and great with kids.'),
(2, 'Luna 2', 4, 'in-shelter', 5, 'female', '2016-10-13', 8.8, '2026-05-19', 'Friendly and great with kids.'),
(3, 'Milo', 2, 'in-shelter', 5, 'male', '2022-06-21', 20.7, '2024-04-11', 'Calm and affectionate lap companion.'),
(4, 'Chloe', 3, 'in-shelter', 2, 'male', '2022-05-27', 11.1, '2025-01-05', 'Shy at first but warms up quickly.'),
(5, 'Lucy 5', 4, 'in-shelter', 3, 'male', '2022-04-30', 2.6, '2025-02-25', 'A bit timid around strangers but loyal once bonded.'),
(6, 'Smokey', 7, 'in-shelter', 3, 'female', '2020-01-21', 10.8, '2025-01-03', 'Calm and affectionate lap companion.'),
(7, 'Oreo', 5, 'in-shelter', 2, 'female', '2024-03-06', 16.0, '2024-05-29', 'Shy at first but warms up quickly.'),
(8, 'Smokey', 3, 'in-shelter', 3, 'female', '2020-09-23', 1.9, '2024-06-07', 'Vaccinated and dewormed, ready for a new home.'),
(9, 'Nala', 6, 'in-shelter', 2, 'female', '2016-10-08', 29.5, '2025-07-06', 'A bit timid around strangers but loyal once bonded.'),
(10, 'Luna', 2, 'in-shelter', 3, 'female', '2023-04-04', 20.4, '2026-07-01', 'Litter trained and very sociable.'),
(11, 'Bantay', 6, 'in-shelter', 3, 'female', '2017-11-19', 21.6, '2026-10-08', 'Friendly and great with kids.'),
(12, 'Buddy', 5, 'in-shelter', 2, 'female', '2020-05-20', 32.1, '2026-10-13', 'Shy at first but warms up quickly.'),
(13, 'Ginger', 7, 'in-shelter', 2, 'male', '2025-03-09', 15.4, '2025-07-24', 'Loves belly rubs and long walks.'),
(14, 'Milo 14', 7, 'in-shelter', 5, 'male', '2017-09-11', 8.5, '2025-04-22', 'Friendly and great with kids.'),
(15, 'Rocky', 3, 'in-shelter', 3, 'male', '2020-09-12', 18.9, '2025-10-14', 'Energetic and loves to play fetch.'),
(16, 'Nala', 9, 'in-shelter', 3, 'male', '2021-02-13', 31.5, '2026-03-14', 'Loves belly rubs and long walks.'),
(17, 'Sadie', 2, 'in-shelter', 2, 'male', '2018-02-19', 2.8, '2025-03-03', 'A bit timid around strangers but loyal once bonded.'),
(18, 'Nala 18', 6, 'in-shelter', 2, 'male', '2022-05-10', 5.7, '2024-07-26', 'Vaccinated and dewormed, ready for a new home.'),
(19, 'Waffles', 2, 'in-shelter', 3, 'female', '2017-08-31', 22.4, '2025-12-12', 'Vaccinated and dewormed, ready for a new home.'),
(20, 'Waffles', 2, 'in-shelter', 3, 'female', '2021-05-21', 17.2, '2024-06-24', 'Energetic and loves to play fetch.'),
(21, 'Tiger', 6, 'in-shelter', 2, 'male', '2021-10-15', 1.3, '2026-01-10', 'Energetic and loves to play fetch.'),
(22, 'Smokey', 1, 'in-shelter', 3, 'male', '2023-10-22', 29.7, '2026-01-21', 'Energetic and loves to play fetch.'),
(23, 'Ginger', 4, 'in-shelter', 2, 'female', NULL, 22.5, '2025-02-03', 'Calm and affectionate lap companion.'),
(24, 'Coco', 4, 'in-shelter', 5, 'female', NULL, 25.7, '2024-02-27', 'Litter trained and very sociable.'),
(25, 'Rocky 25', 8, 'in-shelter', 1, 'female', '2021-01-05', 28.4, '2025-12-16', 'Vaccinated and dewormed, ready for a new home.'),
(26, 'Milo 26', 2, 'in-shelter', 1, 'female', '2018-03-16', 12.2, '2026-09-15', 'Friendly and great with kids.'),
(27, 'Snowy', 8, 'in-shelter', 1, 'male', '2025-05-11', 23.3, '2026-03-06', 'Calm and affectionate lap companion.'),
(28, 'Mocha 28', 8, 'in-shelter', 1, 'female', '2016-12-21', 28.1, '2026-03-21', 'A bit timid around strangers but loyal once bonded.'),
(29, 'Tiger', 7, 'in-shelter', 1, 'male', '2017-11-27', 34.8, '2024-02-26', 'Energetic and loves to play fetch.'),
(30, 'Peanut', 8, 'in-shelter', 2, 'female', '2023-05-16', 32.8, '2024-11-15', 'Energetic and loves to play fetch.'),
(31, 'Bantay', 1, 'in-shelter', 2, 'male', '2021-11-26', 26.4, '2024-10-12', 'Loves belly rubs and long walks.'),
(32, 'Biscuit', 4, 'in-shelter', 3, 'male', '2018-10-28', 7.8, '2026-10-23', 'Calm and affectionate lap companion.'),
(33, 'Rocky', 6, 'in-shelter', 3, 'male', '2016-09-06', 31.9, '2025-12-25', 'A bit timid around strangers but loyal once bonded.'),
(34, 'Molly', 9, 'in-shelter', 3, 'male', '2021-12-18', 5.7, '2026-11-11', 'Friendly and great with kids.'),
(35, 'Smokey 35', 8, 'in-shelter', 3, 'male', '2024-09-13', 28.1, '2024-12-18', 'Energetic and loves to play fetch.'),
(36, 'Nala', 8, 'in-shelter', 3, 'male', '2019-08-28', 24.0, '2026-09-15', 'Shy at first but warms up quickly.'),
(37, 'Luna', 9, 'in-shelter', 3, 'female', '2016-06-21', 27.1, '2026-11-05', 'A bit timid around strangers but loyal once bonded.'),
(38, 'Bantay', 9, 'in-shelter', 3, 'male', '2020-12-20', 11.7, '2026-11-01', 'Calm and affectionate lap companion.'),
(39, 'Duke', 5, 'in-shelter', 3, 'female', '2021-09-10', 33.0, '2025-06-15', 'Calm and affectionate lap companion.'),
(40, 'Buddy', 8, 'in-shelter', 3, 'female', '2020-12-15', 11.4, '2025-05-07', 'Loves belly rubs and long walks.'),
(41, 'Coco', 2, 'in-shelter', 3, 'male', '2026-01-22', 27.3, '2026-01-23', 'Energetic and loves to play fetch.'),
(42, 'Mocha 42', 5, 'in-shelter', 5, 'female', '2018-06-18', 26.3, '2024-07-11', 'Loves belly rubs and long walks.'),
(43, 'Mittens', 3, 'in-shelter', 5, 'male', '2023-12-03', 15.4, '2026-04-07', 'Vaccinated and dewormed, ready for a new home.'),
(44, 'Lucy', 4, 'in-shelter', 5, 'female', '2016-03-20', 12.2, '2026-07-28', 'A bit timid around strangers but loyal once bonded.'),
(45, 'Bear', 7, 'in-shelter', 1, 'female', '2021-09-29', 33.6, '2024-08-19', 'Calm and affectionate lap companion.'),
(46, 'Rocky', 2, 'in-shelter', 1, 'male', '2019-01-12', 26.6, '2026-05-14', 'Litter trained and very sociable.'),
(47, 'Ginger', 3, 'in-shelter', 3, 'female', NULL, 24.7, '2024-07-02', 'Litter trained and very sociable.');


-- ============================================================
-- staffroles
-- ============================================================
INSERT INTO pet_adoption_staffrole (id, role_name) VALUES
(1, 'Manager'),
(2, 'Veterinarian'),
(3, 'Counselor'),
(4, 'Intern'),
(5, 'Assistant');

-- ============================================================
-- staffs
-- ============================================================
INSERT INTO pet_adoption_staff (id, first_name, last_name, date_of_birth, sex, email, contact_number, address, role_id, status, shelter_id, hire_date) VALUES
(1, 'Maria', 'Santos', '1985-03-14', 'female', 'maria.santos@pawshaven.ph', '09171234501', '12 Rizal St, Quezon City', 1, 'active', 1, '2019-06-01'),
(2, 'Jose', 'Reyes', '1990-07-22', 'male', 'jose.reyes@pawshaven.ph', '09171234502', '34 Luna St, Makati City', 2, 'active', 2, '2020-02-15'),
(3, 'Ana', 'Bautista', '1992-11-05', 'female', 'ana.bautista@pawshaven.ph', '09171234503', '56 Bonifacio Ave, Cavite', 3, 'active', 1, '2021-04-10'),
(4, 'Carlos', 'Cruz', '1988-01-30', 'male', 'carlos.cruz@pawshaven.ph', '09171234504', '78 Del Pilar St, Cebu City', 3, 'active', 3, '2018-09-20'),
(5, 'Rosa', 'Villanueva', '1995-05-18', 'female', 'rosa.villanueva@pawshaven.ph', '09171234505', '90 Aguinaldo Hwy, Cavite', 4, 'on-leave', 4, '2022-03-05'),
(6, 'Pedro', 'Garcia', '1983-09-09', 'male', 'pedro.garcia@pawshaven.ph', '09171234506', '11 Osmena Blvd, Cebu City', 5, 'terminated', 5, '2017-01-12'),
(7, 'Carmen', 'Flores', '1993-12-02', 'female', 'carmen.flores@pawshaven.ph', '09171234509', '44 Quezon Ave, QC', 1, 'active', 5, '2023-01-09');


-- ============================================================
-- adopters
-- ============================================================
INSERT INTO pet_adoption_adopter (id, first_name, last_name, date_of_birth, sex, email, contact_number, address) VALUES
(1, 'Jose', 'Mendoza', '1998-02-26', 'male', 'josemendoza1@gmail.com', '09401419314', '884 Mabini Ave, Pasig'),
(2, 'Maria', 'Ramos', '1997-06-24', 'female', 'mariaramos2@gmail.com', '09920831240', '186 Osmena Ave, Makati'),
(3, 'Ricardo', 'Gonzales', '1978-06-20', 'female', 'ricardogonzales3@gmail.com', '09782450400', '19 Taft Ave, Cebu City'),
(4, 'Pedro', 'Navarro', '2002-08-04', 'male', 'pedronavarro4@gmail.com', '09716786843', '236 Magsaysay Ave, Manila'),
(5, 'Fernando', 'Garcia', '1996-04-22', 'female', 'fernandogarcia5@gmail.com', '09020146201', '682 Quezon Ave, Cebu City'),
(6, 'Laura', 'Gonzales', '1981-09-23', 'female', 'lauragonzales6@gmail.com', '09072247045', '985 Magsaysay Ave, Cebu City'),
(7, 'Miguel', 'Flores', '1963-02-02', 'female', 'miguelflores7@gmail.com', '09352056174', '515 Osmena Ave, Manila'),
(8, 'Ramon', 'Santos', '1968-02-25', 'female', 'ramonsantos8@gmail.com', '09126906044', '645 Osmena Ave, Quezon City'),
(9, 'Eduardo', 'Navarro', '1973-12-05', 'female', 'eduardonavarro9@gmail.com', '09572492086', '752 Taft Ave, Manila'),
(10, 'Ramon', 'Navarro', '1961-06-10', 'male', 'ramonnavarro10@gmail.com', '09100251678', '52 Mabini Ave, Cavite'),
(11, 'Patricia', 'Flores', '2003-11-24', 'female', 'patriciaflores11@gmail.com', '09071881817', '259 Mabini Ave, Makati'),
(12, 'Elena', 'Torres', '1980-09-12', 'female', 'elenatorres12@gmail.com', '09761740931', '615 Osmena Ave, Makati'),
(13, 'Luis', 'Gonzales', '1971-12-21', 'male', 'luisgonzales13@gmail.com', '09707413748', '293 Quezon Ave, Pasig'),
(14, 'Francisco', 'Bautista', '1977-11-16', 'female', 'franciscobautista14@gmail.com', '09170471874', '397 Osmena Ave, Manila'),
(15, 'Juan', 'Cruz', '1972-09-18', 'female', 'juancruz15@gmail.com', '09529841537', '920 Quezon Ave, Pasig'),
(16, 'Maria', 'Mendoza', '1960-04-27', 'female', 'mariamendoza16@gmail.com', '09764265651', '861 Magsaysay Ave, Quezon City'),
(17, 'Miguel', 'Ramos', '1995-09-24', 'male', 'miguelramos17@gmail.com', '09304451669', '79 Magsaysay Ave, Pasig'),
(18, 'Roberto', 'Rivera', '1964-04-30', 'female', 'robertorivera18@gmail.com', '09104234685', '195 Magsaysay Ave, Pasig'),
(19, 'Maria', 'Dela Cruz', '1978-04-02', 'male', 'mariadelacruz19@gmail.com', '09067924708', '131 Osmena Ave, Pasig'),
(20, 'Isabel', 'Ramos', '1985-04-11', 'female', 'isabelramos20@gmail.com', '09446347861', '172 Osmena Ave, Quezon City');

-- ============================================================
-- adoptions
-- ============================================================
INSERT INTO pet_adoption_adoption (id, pet_id, adopter_id, staff_id, request_date, adoption_date, status) VALUES
(1, 1, 6, 1, '2026-05-04', '2026-05-04', 'completed'), -- same-day turnaround
(2, 2, 7, 2, '2025-12-01', NULL, 'pending'), -- long-stale pending request
(3, 3, 8, 1, '2026-06-10', '2026-07-01', 'completed'), -- maximum (21-day) processing time,
(4, 4, 9, 1,  '2024-02-29', '2024-03-08', 'completed'), -- request filed on a leap day (2024-02-29),
(5, 5, 10, 2,  '2026-01-10', NULL, 'rejected'), -- first attempt on this pet - rejected,
(6, 5, 11, 2, '2026-03-22', '2026-04-01', 'completed'), -- second attempt on same pet - completed,
(7, 6, 1, 5, '2025-09-01', '2025-09-07', 'completed'), -- repeat adopter - pet #1,
(8, 7, 1, 5, '2026-04-18', '2026-04-22', 'completed'), -- repeat adopter - pet #2,
(9, 8, 13, 1, '2026-11-05', '2026-11-11', 'completed'), -- completed this month,
(10, 9, 14, 2, '2026-03-03', '2026-03-12', 'completed'), -- completed this year, different month,
(11, 10, 15, 3, '2024-06-15', '2024-06-29', 'completed'), -- completed in 2024,
(12, 11, 16, 1, '2025-08-20', '2025-08-31', 'completed'), -- completed in 2025,
(13, 12, 17, 2, '2026-10-20', NULL, 'approved'), -- approved, pickup not yet completed,
(14, 13, 18, 5, '2026-11-01', NULL, 'pending'), -- recent pending request,
(15, 14, 19, 1, '2026-02-14', NULL, 'rejected'), -- application rejected,
(16, 15, 1, 3, '2026-02-05', '2026-02-12', 'completed'), -- tie scenario - Bautista #1,
(17, 16, 3, 3, '2026-05-19', '2026-05-24', 'completed'), -- tie scenario - Bautista #2,
(18, 17, 4, 4, '2026-03-12', '2026-03-19', 'completed'), -- tie scenario - Cruz #1,
(19, 18, 5, 4, '2026-08-09', '2026-08-14', 'completed'), -- tie scenario - Cruz #2,
(20, 19, 10, 5, '2026-09-01', '2026-09-04', 'completed'), -- pet adopted the same day it was taken in,
(21, 7, 17, 6, '2025-06-20', NULL, 'approved'),
(22, 15, 14, 2, '2025-03-31', '2025-04-11', 'completed'),
(23, 18, 3, 5, '2025-10-19', '2025-10-26', 'completed'),
(24, 1, 14, 6, '2025-07-12', '2025-07-21', 'completed'),
(25, 11, 2, 6, '2026-03-06', '2026-03-23', 'completed'),
(26, 17, 7, 1, '2025-07-24', '2025-08-14', 'completed'),
(27, 15, 14, 5, '2026-01-12', NULL, 'rejected'),
(28, 5, 2, 6, '2026-08-31', NULL, 'pending'),
(29, 19, 16, 1, '2026-09-28', '2026-10-13', 'completed'),
(30, 15, 8, 1, '2024-12-15', '2024-12-19', 'completed');

-- Reconcile pet status with adoption outcomes (For adopted and deceased)
UPDATE pet_adoption_pet SET status = 'adopted' WHERE id IN (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19);
UPDATE pet_adoption_pet SET status = 'deceased' WHERE id IN (43, 44, 45, 46);