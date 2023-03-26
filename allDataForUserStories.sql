PRAGMA foreign_keys = ON;
PRAGMA foreign_key_check;

-- USERSTORY A
BEGIN;
PRAGMA defer_foreign_keys = 1;

INSERT INTO Stasjon (Stasjonsnavn, moh)
VALUES 
('Bodoe', 4.1),
('Fauske', 34.0),
('Mo I Rana', 3.5),
('Mosjoeen', 6.8),
('Steinkjer', 3.0),
('Trondheim', 5.1);

INSERT INTO Delstrekning (StartStasjon, Endestasjon, SporType, Lengde)
VALUES
('Bodoe', 'Fauske', 'Enkel', 60),
('Fauske', 'Mo I Rana', 'Enkel', 170),
('Mo I Rana', 'Mosjoeen', 'Enkel', 90),
('Mosjoeen', 'Steinkjer', 'Enkel', 280),
('Steinkjer', 'Trondheim', 'Dobbel', 120);

INSERT INTO Banestrekning (Banenavn, Fremdriftsenergi)
VALUES ('Nordlandsbanen', 'Diesel');

INSERT INTO BanePasserer (Banenavn, Stasjonsnavn, Stasjonsnummer)
VALUES
('Nordlandsbanen', 'Trondheim', 0),
('Nordlandsbanen', 'Steinkjer', 1),
('Nordlandsbanen', 'Mosjoeen', 2),
('Nordlandsbanen', 'Mo I Rana', 3),
('Nordlandsbanen', 'Fauske', 4),
('Nordlandsbanen', 'Bodoe', 5);

-- USERSTORY B
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
(1, 'Mosjoeen', 2),
(1, 'Mo I Rana', 3),
(1, 'Fauske', 4),
(1, 'Bodoe', 5),
(2, 'Trondheim', 0),
(2, 'Steinkjer', 1),
(2, 'Mosjoeen', 2),
(2, 'Mo I Rana', 3),
(2, 'Fauske', 4),
(2, 'Bodoe', 5),
(3, 'Mo I Rana', 0),
(3, 'Mosjoeen', 1),
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
(1, 'Mosjoeen', 'Mandag', '13:20', '13:20'),
(1, 'Mosjoeen', 'Tirsdag', '13:20', '13:20'),
(1, 'Mosjoeen', 'Onsdag', '13:20', '13:20'),
(1, 'Mosjoeen', 'Torsdag', '13:20', '13:20'),
(1, 'Mosjoeen', 'Fredag', '13:20', '13:20'),
(1, 'Mo I Rana', 'Mandag', '14:31', '14:31'),
(1, 'Mo I Rana', 'Tirsdag', '14:31', '14:31'),
(1, 'Mo I Rana', 'Onsdag', '14:31', '14:31'),
(1, 'Mo I Rana', 'Torsdag', '14:31', '14:31'),
(1, 'Mo I Rana', 'Fredag', '14:31', '14:31'),
(1, 'Fauske', 'Mandag', '16:49', '16:49'),
(1, 'Fauske', 'Tirsdag', '16:49', '16:49'),
(1, 'Fauske', 'Onsdag', '16:49', '16:49'),
(1, 'Fauske', 'Torsdag', '16:49', '16:49'),
(1, 'Fauske', 'Fredag', '16:49', '16:49'),
(1, 'Bodoe', 'Mandag', '17:34', NULL),
(1, 'Bodoe', 'Tirsdag', '17:34', NULL),
(1, 'Bodoe', 'Onsdag', '17:34', NULL),
(1, 'Bodoe', 'Torsdag', '17:34', NULL),
(1, 'Bodoe', 'Fredag', '17:34', NULL),

(2, 'Trondheim', 'Mandag', NULL, '23:05'),
(2, 'Trondheim', 'Tirsdag', NULL, '23:05'),
(2, 'Trondheim', 'Onsdag', NULL, '23:05'),
(2, 'Trondheim', 'Torsdag', NULL, '23:05'),
(2, 'Trondheim', 'Fredag', NULL, '23:05'),
(2, 'Trondheim', 'Loerdag', NULL, '23:05'),
(2, 'Trondheim', 'Soendag', NULL, '23:05'),
(2, 'Steinkjer', 'Mandag', '00:57', '00:57'),
(2, 'Steinkjer', 'Tirsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Onsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Torsdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Fredag', '00:57', '00:57'),
(2, 'Steinkjer', 'Loerdag', '00:57', '00:57'),
(2, 'Steinkjer', 'Soendag', '00:57', '00:57'),
(2, 'Mosjoeen', 'Mandag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Tirsdag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Onsdag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Torsdag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Fredag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Loerdag', '04:41', '04:41'),
(2, 'Mosjoeen', 'Soendag', '04:41', '04:41'),
(2, 'Mo I Rana', 'Mandag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Tirsdag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Onsdag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Torsdag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Fredag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Loerdag', '05:55', '05:55'),
(2, 'Mo I Rana', 'Soendag', '05:55', '05:55'),
(2, 'Fauske', 'Mandag', '08:19', '08:19'),
(2, 'Fauske', 'Tirsdag', '08:19', '08:19'),
(2, 'Fauske', 'Onsdag', '08:19', '08:19'),
(2, 'Fauske', 'Torsdag', '08:19', '08:19'),
(2, 'Fauske', 'Fredag', '08:19', '08:19'),
(2, 'Fauske', 'Loerdag', '08:19', '08:19'),
(2, 'Fauske', 'Soendag', '08:19', '08:19'),
(2, 'Bodoe', 'Mandag', '09:05', NULL),
(2, 'Bodoe', 'Tirsdag', '09:05', NULL),
(2, 'Bodoe', 'Onsdag', '09:05', NULL),
(2, 'Bodoe', 'Torsdag', '09:05', NULL),
(2, 'Bodoe', 'Fredag', '09:05', NULL),
(2, 'Bodoe', 'Loerdag', '09:05', NULL),
(2, 'Bodoe', 'Soendag', '09:05', NULL),

(3, 'Mo I Rana', 'Mandag', NULL, '08:11'),
(3, 'Mo I Rana', 'Tirsdag', NULL, '08:11'),
(3, 'Mo I Rana', 'Onsdag', NULL, '08:11'),
(3, 'Mo I Rana', 'Torsdag', NULL, '08:11'),
(3, 'Mo I Rana', 'Fredag', NULL, '08:11'),
(3, 'Mosjoeen', 'Mandag', '09:14', '09:14'),
(3, 'Mosjoeen', 'Tirsdag', '09:14', '09:14'),
(3, 'Mosjoeen', 'Onsdag', '09:14', '09:14'),
(3, 'Mosjoeen', 'Torsdag', '09:14', '09:14'),
(3, 'Mosjoeen', 'Fredag', '09:14', '09:14'),
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

-- USERSTORY F
INSERT INTO Togtur (TurID, TurDato, RuteID)
VALUES 
(1, '2023-04-03', 1),
(2, '2023-04-04', 1),
(3, '2023-04-03', 2),
(4, '2023-04-04', 2),
(5, '2023-04-03', 3),
(6, '2023-04-04', 3);

COMMIT;