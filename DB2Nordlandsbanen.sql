PRAGMA foreign_keys = ON;
PRAGMA foreign_key_check;

CREATE TABLE IF NOT EXISTS Stasjon (
	Stasjonsnavn VARCHAR(255) NOT NULL,
	Moh FLOAT(1) NOT NULL,
	PRIMARY KEY(Stasjonsnavn)
);

CREATE TABLE IF NOT EXISTS Delstrekning (
	StartStasjon VARCHAR(255) NOT NULL, 
	Endestasjon VARCHAR(255) NOT NULL, 
	SporType VARCHAR(255) NOT NULL CHECK(SporType = 'Enkel' OR SporType = 'Dobbel'),
	Lengde INTEGER NOT NULL CHECK(Lengde > 0),
	PRIMARY KEY (StartStasjon, Endestasjon),
	FOREIGN KEY (StartStasjon) REFERENCES Stasjon(Stasjonsnavn) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (Endestasjon) REFERENCES Stasjon(Stasjonsnavn) ON DELETE CASCADE ON UPDATE CASCADE,
	CHECK (StartStasjon <> Endestasjon)
);

CREATE TABLE IF NOT EXISTS Banestrekning (
	Banenavn VARCHAR(255) NOT NULL, 
	Fremdriftsenergi VARCHAR(255) NOT NULL,
	PRIMARY KEY(Banenavn)
);

CREATE TABLE IF NOT EXISTS BanePasserer (
	Banenavn VARCHAR(255) NOT NULL, 
	Stasjonsnavn VARCHAR(255) NOT NULL, 
	Stasjonsnummer INTEGER NOT NULL,
	PRIMARY KEY(Banenavn, Stasjonsnavn),
	FOREIGN KEY (Stasjonsnavn) REFERENCES Stasjon(Stasjonsnavn) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (Banenavn) REFERENCES Banestrekning(Banenavn) ON DELETE CASCADE ON UPDATE CASCADE
	UNIQUE(Banenavn, Stasjonsnummer)
);
 
CREATE TABLE IF NOT EXISTS Togrute (
	RuteID INTEGER NOT NULL, 
	BaneRetning VARCHAR(255) NOT NULL CHECK(BaneRetning = 'Mot' OR BaneRetning = 'Med'),
	VognOppsettID INTEGER NOT NULL,
	PRIMARY KEY(RuteID),
	FOREIGN KEY (VognOppsettID) REFERENCES VognOppsett(VognOppsettID) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS RutePaaBane (
	RuteID INTEGER NOT NULL, 
	Banenavn VARCHAR(255) NOT NULL,
	PRIMARY KEY(RuteID, Banenavn),
	FOREIGN KEY(RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(Banenavn) REFERENCES Banestrekning(Banenavn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Rutestopp (
	RuteID INTEGER NOT NULL, 
	Stasjonsnavn VARCHAR(255) NOT NULL, 
	StoppNr INTEGER NOT NULL,
	PRIMARY KEY(RuteID, Stasjonsnavn),
	FOREIGN KEY(RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE, 
	FOREIGN KEY(Stasjonsnavn) REFERENCES Stasjon(Stasjonsnavn) ON DELETE CASCADE ON UPDATE CASCADE
	UNIQUE(RuteID, StoppNr)
);

CREATE TABLE IF NOT EXISTS Rutetider (
	RuteID INTEGER NOT NULL, 
	Stasjonsnavn VARCHAR(255) NOT NULL, 
	Ukedag VARCHAR(255) NOT NULL CHECK (Ukedag = 'Mandag' OR Ukedag = 'Tirsdag' OR Ukedag = 'Onsdag' OR Ukedag = 'Torsdag' OR Ukedag = 'Fredag' OR Ukedag = 'Loerdag' OR Ukedag = 'Soendag'),
	Ankomst TIME, -- Must be able to be null
	Avgang TIME, -- Must be able to be null
	PRIMARY KEY(RuteID, Stasjonsnavn, Ukedag),
	FOREIGN KEY(RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(Stasjonsnavn) REFERENCES Stasjon(Stasjonsnavn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Togtur (
	TurID INTEGER NOT NULL, 
	TurDato DATE NOT NULL, 
	RuteID INTEGER NOT NULL,
	PRIMARY KEY(TurID),
	FOREIGN KEY(RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS VognOppsett (
	VognOppsettID INTEGER NOT NULL, 
	Operatoer VARCHAR(255) NOT NULL,
	PRIMARY KEY(VognOppsettID)
);

CREATE TABLE IF NOT EXISTS Vogn (
	VognNavn VARCHAR(255) NOT NULL, 
	VognType VARCHAR(255) NOT NULL CHECK(VognType ='Sittevogn' OR VognType = 'Sovevogn'),
	AntallGrupperinger INTEGER NOT NULL, 
	PlasserPerGruppering INTEGER NOT NULL, 
	Operatoer VARCHAR(255) NOT NULL,
	PRIMARY KEY(VognNavn)
);

CREATE TABLE IF NOT EXISTS VognForekomst (
	VognOppsettID INTEGER NOT NULL, 
	VognNummer INTEGER NOT NULL, 
	VognNavn VARCHAR(255) NOT NULL,
	PRIMARY KEY(VognOppsettID, VognNummer),
	FOREIGN KEY(VognNavn) REFERENCES Vogn(VognNavn) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY(VognOppsettID) REFERENCES VognOppsett(VognOppsettID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Kunde (
	Kundenummer INTEGER NOT NULL, 
	Navn VARCHAR(255) NOT NULL, 
	Epost VARCHAR(255) NOT NULL, 
	TlfNr VARCHAR(255) NOT NULL,
	PRIMARY KEY(Kundenummer),
	UNIQUE(Epost),
	UNIQUE(TlfNr)
);

CREATE TABLE IF NOT EXISTS KundeOrdre (
	Ordrenummer INTEGER NOT NULL, 
	KjoepsTidspunkt DATETIME NOT NULL, 
	Kundenummer INTEGER NOT NULL,
	PRIMARY KEY(Ordrenummer),
	FOREIGN KEY(Kundenummer) REFERENCES Kunde(Kundenummer) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Billett (
	TurID INTEGER NOT NULL, 
	BillettID INTEGER NOT NULL,
	OrdreNummer INTEGER NOT NULL, 
	PlassNummer INTEGER NOT NULL, 
	VognNummer INTEGER NOT NULL, 
	PRIMARY KEY(TurID, BillettID),
	FOREIGN KEY(TurID) REFERENCES Togtur(TurID) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY(OrdreNummer) REFERENCES KundeOrdre(OrdreNummer) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS BillettStopperVed (
	TurID INTEGER NOT NULL, 
	BillettID INTEGER NOT NULL, 
	Stasjonsnavn VARCHAR(255) NOT NULL, 
	StasjonsNummer INTEGER NOT NULL,
	PRIMARY KEY(TurID, BillettID, Stasjonsnavn),
	UNIQUE(TurID, BillettID, StasjonsNummer),
	FOREIGN KEY(TurID, BillettID) REFERENCES Billett(TurID, BillettID) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY(Stasjonsnavn) REFERENCES Stasjon(Stasjonsnavn) ON DELETE RESTRICT ON UPDATE CASCADE
);
