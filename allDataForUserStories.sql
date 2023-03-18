-- USERSSTORY A
INSERT INTO Stasjon (Stasjonsnavn, moh)
VALUES 
('Bodø', 4.1),
('Fauske', 34.0),
('Mo i Rana', 3.5),
('Mosjøen', 6.8),
('Steinkjer', 3.0),
('Trondheim', 5.1);

INSERT INTO Delstrekning (StartStasjon, Endestasjon, SporType, Lengde)
VALUES
('Bodø', 'Fauske', 'Enkel', 60),
('Fauske', 'Mo i Rana', 'Enkel', 170),
('Mo i Rana', 'Mosjøen', 'Enkel', 90),
('Mosjøen', 'Steinkjer', 'Enkel', 280),
('Steinkjer', 'Trondheim', 'Dobbel', 120);

INSERT INTO Banestrekning (Banenavn, Fremdriftsenergi)
VALUES ('Nordlandsbanen', 'Diesel');

INSERT INTO BanePasserer (Banenavn, Stasjonsnavn, Stasjonsnummer)
VALUES
('Nordlandsbanen', 'Trondheim', 0),
('Nordlandsbanen', 'Steinkjer', 1),
('Nordlandsbanen', 'Mosjøen', 2),
('Nordlandsbanen', 'Mo i Rana', 3),
('Nordlandsbanen', 'Fauske', 4),
('Nordlandsbanen', 'Bodø', 5);

-- USERSSTORY B
INSERT INTO Togrute (RuteID, BaneRetning, VognOppsettID)
VALUES
(1, 'Med', 1),
(2, 'Med', 2),
(3, 'Mot', 3);

INSERT INTO RutePaaBane (RuteID, Banenavn)
VALUES 
(1, 'Nordlandsbanen'),
(2, 'Nordlandsbanen'),
(3, 'Nordlandsbanen');

INSERT INTO Rutestopp(RuteID, Stasjonsnavn, StoppNr)
VALUES
(1, 'Trondheim', 0),
(1, 'Steinkjer', 1),
(1, 'Mosjøen', 2),
(1, 'Mo i Rana', 3),
(1, 'Fauske', 4),
(1, 'Bodø', 5),
(2, 'Trondheim', 0),
(2, 'Steinkjer', 1),
(2, 'Mosjøen', 2),
(2, 'Mo i Rana', 3),
(2, 'Fauske', 4),
(2, 'Bodø', 5),
(3, 'Mo i Rana', 0),
(3, 'Mosjøen', 1),
(3, 'Steinkjer', 2),
(3, 'Trondheim', 3);

INSERT INTO Rutetider (RuteID, Stasjonsnavn, Ukedag, Ankomst, Avgang)
VALUES
(1, 'Trondheim', 'Mandag', NULL, '07:49'),
(1, 'Trondheim', 'Tirsdag', NULL, '07:49'),
(1, 'Trondheim', 'Onsdag', NULL, '07:49'),
(1, 'Trondheim', 'Torsdag', NULL, '07:49'),
(1, 'Trondheim', 'Fredag', NULL, '07:49'),
(1, 'Steinkjer', 'Mandag', '09:51', '09:51'),
(1, 'Steinkjer', 'Tirsdag', '09:51', '09:51'),
(1, 'Steinkjer', 'Onsdag', '09:51', '09:51'),
(1, 'Steinkjer', 'Torsdag', '09:51', '09:51'),
(1, 'Steinkjer', 'Fredag', '09:51', '09:51'),
(1, 'Mosjøen', 'Mandag', '13:20', '13:20'),
(1, 'Mosjøen', 'Tirsdag', '13:20', '13:20'),
(1, 'Mosjøen', 'Onsdag', '13:20', '13:20'),
(1, 'Mosjøen', 'Torsdag', '13:20', '13:20'),
(1, 'Mosjøen', 'Fredag', '13:20', '13:20'),
(1, 'Mo i Rana', 'Mandag', '14:31', '14:31'),
(1, 'Mo i Rana', 'Tirsdag', '14:31', '14:31'),
(1, 'Mo i Rana', 'Onsdag', '14:31', '14:31'),
(1, 'Mo i Rana', 'Torsdag', '14:31', '14:31'),
(1, 'Mo i Rana', 'Fredag', '14:31', '14:31'),
(1, 'Fauske', 'Mandag', '16:49', '16:49'),
(1, 'Fauske', 'Tirsdag', '16:49', '16:49'),
(1, 'Fauske', 'Onsdag', '16:49', '16:49'),
(1, 'Fauske', 'Torsdag', '16:49', '16:49'),
(1, 'Fauske', 'Fredag', '16:49', '16:49'),
(1, 'Bodø', 'Mandag', '17:34', NULL),
(1, 'Bodø', 'Tirsdag', '17:34', NULL),
(1, 'Bodø', 'Onsdag', '17:34', NULL),
(1, 'Bodø', 'Torsdag', '17:34', NULL),
(1, 'Bodø', 'Fredag', '17:34', NULL),

(2, 'Trondheim', 'Mandag', NULL, '23:05'),
(2, 'Trondheim', 'Tirsdag', NULL, '23:05'),
(2, 'Trondheim', 'Onsdag', NULL, '23:05'),
(2, 'Trondheim', 'Torsdag', NULL, '23:05'),
(2, 'Trondheim', 'Fredag', NULL, '23:05'),
(2, 'Trondheim', 'Lørdag', NULL, '23:05'),
(2, 'Trondheim', 'Søndag', NULL, '23:05'),
(2, 'Steinkjer', 'Mandag', '00:57', '00:57'),
(2, 'Steinkjer', 'Tirsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Onsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Torsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Fredag', '00:57', '00:57'),
(2, 'Steinkjer', 'Lørdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Søndag', '00:57', '00:57'),
(2, 'Mosjøen', 'Mandag', '04:41', '04:41'),
(2, 'Mosjøen', 'Tirsdag', '04:41', '04:41'),
(2, 'Mosjøen', 'Onsdag', '04:41', '04:41'),
(2, 'Mosjøen', 'Torsdag', '04:41', '04:41'),
(2, 'Mosjøen', 'Fredag', '04:41', '04:41'),
(2, 'Mosjøen', 'Lørdag', '04:41', '04:41'),
(2, 'Mosjøen', 'Søndag', '04:41', '04:41'),
(2, 'Mo i Rana', 'Mandag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Tirsdag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Onsdag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Torsdag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Fredag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Lørdag', '05:55', '05:55'),
(2, 'Mo i Rana', 'Søndag', '05:55', '05:55'),
(2, 'Fauske', 'Mandag', '08:19', '08:19'),
(2, 'Fauske', 'Tirsdag', '08:19', '08:19'),
(2, 'Fauske', 'Onsdag', '08:19', '08:19'),
(2, 'Fauske', 'Torsdag', '08:19', '08:19'),
(2, 'Fauske', 'Fredag', '08:19', '08:19'),
(2, 'Fauske', 'Lørdag', '08:19', '08:19'),
(2, 'Fauske', 'Søndag', '08:19', '08:19'),
(2, 'Bodø', 'Mandag', '09:05', NULL),
(2, 'Bodø', 'Tirsdag', '09:05', NULL),
(2, 'Bodø', 'Onsdag', '09:05', NULL),
(2, 'Bodø', 'Torsdag', '09:05', NULL),
(2, 'Bodø', 'Fredag', '09:05', NULL),
(2, 'Bodø', 'Lørdag', '09:05', NULL),
(2, 'Bodø', 'Søndag', '09:05', NULL),

(3, 'Mo i Rana', 'Mandag', NULL, '08:11'),
(3, 'Mo i Rana', 'Tirsdag', NULL, '08:11'),
(3, 'Mo i Rana', 'Onsdag', NULL, '08:11'),
(3, 'Mo i Rana', 'Torsdag', NULL, '08:11'),
(3, 'Mo i Rana', 'Fredag', NULL, '08:11'),
(3, 'Mosjøen', 'Mandag', '09:14', '09:14'),
(3, 'Mosjøen', 'Tirsdag', '09:14', '09:14'),
(3, 'Mosjøen', 'Onsdag', '09:14', '09:14'),
(3, 'Mosjøen', 'Torsdag', '09:14', '09:14'),
(3, 'Mosjøen', 'Fredag', '09:14', '09:14'),
(3, 'Steinkjer', 'Mandag', '12:31', '12:31'),
(3, 'Steinkjer', 'Tirsdag', '12:31', '12:31'),
(3, 'Steinkjer', 'Onsdag', '12:31', '12:31'),
(3, 'Steinkjer', 'Torsdag', '12:31', '12:31'),
(3, 'Steinkjer', 'Fredag', '12:31', '12:31'),
(3, 'Trondheim', 'Mandag', '12:31', NULL),
(3, 'Trondheim', 'Tirsdag', '12:31', NULL),
(3, 'Trondheim', 'Onsdag', '12:31', NULL),
(3, 'Trondheim', 'Torsdag', '12:31', NULL),
(3, 'Trondheim', 'Fredag', '12:31', NULL);

INSERT INTO VognOppsett (VognOppsettID, Operatoer)
VALUES
(1, 'SJ'),
(2, 'SJ'),
(3, 'SJ');

INSERT INTO Vogn (VognNavn, VognType, AntallGrupperinger, PlasserPerGruppering, Operatoer)
VALUES
('SJ-Sittevogn-1', 'Sittevogn', 3, 4, 'SJ'),
('SJ-Sovevogn-1', 'Sovevogn', 4, 2, 'SJ');

INSERT INTO VognForekomst (VognOppsettID, VognNummer, VognNavn)
VALUES
(1, 1, 'SJ-Sittevogn-1'),
(1, 2, 'SJ-Sittevogn-1'),
(2, 1, 'SJ-Sittevogn-1'),
(2, 2, 'SJ-Sovevogn-1'),
(3, 1, 'SJ-Sittevogn-1');

-- USERSSTORY F
INSERT INTO Togtur (TurID, TurDato, RuteID)
VALUES 
(1, '2023-04-03', 1),
(2, '2023-04-04', 1),
(3, '2023-04-03', 2),
(4, '2023-04-04', 2),
(5, '2023-04-03', 3),
(6, '2023-04-04', 3);
