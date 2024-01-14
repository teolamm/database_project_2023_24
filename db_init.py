'''database init in python'''

import sqlite3 as sql

class Initialisation:
	def __init__(self):

		self.conn = sql.connect("ev.db")

		self.conn.execute('''CREATE TABLE ΙΔΙΟΚΤΗΤΗΣ
    	("όνομα"	TEXT NOT NULL,
		"επίθετο"	TEXT NOT NULL,
		"id"	INTEGER NOT NULL,
		"email"	TEXT NOT NULL,
		"τηλ"	INTEGER NOT NULL,
		"τόπος"	TEXT,
		"ημ_δημιουργίας_λογαριασμού"	TEXT,
		PRIMARY KEY("id" AUTOINCREMENT));''')

		self.conn.execute('''CREATE TABLE ΑΥΤΟΚΙΝΗΤΟ (
		"πινακίδες"	TEXT NOT NULL,
		"μάρκα"	TEXT NOT NULL,
		"μοντέλο"	TEXT NOT NULL,
		"έτος_κατασκευής"	TEXT NOT NULL,
		"id_οδηγού"	INTEGER NOT NULL,
		FOREIGN KEY("id_οδηγού") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("πινακίδες"));
	''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΕΚΤΕΛΕΙ (
		"id_οδηγού"	INTEGER NOT NULL,
		"αριθμός_φόρτισης"	INTEGER NOT NULL,
		PRIMARY KEY("id_οδηγού","αριθμός_φόρτισης"),
		FOREIGN KEY("id_οδηγού") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY("αριθμός_φόρτισης") REFERENCES "ΠΛΗΡΩΜΗ"("αριθμός_φόρτισης") ON DELETE CASCADE ON UPDATE CASCADE);
	''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΘΕΣΗ (
		"αριθμός_θέσης"	INTEGER NOT NULL,
		"κατειλημμένη"	INTEGER DEFAULT 0,
		"id_σταθμού"	INTEGER,
		"τύπος_φορτιστή"	TEXT NOT NULL,
		"χρέωση_ανά_τύπο"	TEXT,
		FOREIGN KEY("id_σταθμού") REFERENCES "ΣΤΑΘΜΟΣ"("id_σταθμού") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("αριθμός_θέσης")
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΚΑΡΤΑ (
		"ονοματεπώνυμο_κατόχου"	TEXT NOT NULL,
		"αριθμός_κάρτας"	INTEGER NOT NULL,
		"ημερομηνία_λήξης"	TEXT NOT NULL,
		"CVC"	INTEGER NOT NULL,
		"id_κατόχου"	INTEGER NOT NULL,
		FOREIGN KEY("id_κατόχου") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("αριθμός_κάρτας")
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΚΡΙΤΙΚΗ (
		"id_κριτικής"	INTEGER NOT NULL,
		"αστέρια"	INTEGER NOT NULL,
		"ημερομηνία_κριτικής"	TEXT,
		"id_οδηγού"	INTEGER NOT NULL,
		"id_σταθμού"	INTEGER NOT NULL,
		PRIMARY KEY("id_κριτικής"),
		FOREIGN KEY("id_οδηγού") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY("id_σταθμού") REFERENCES "ΣΤΑΘΜΟΣ"("id_σταθμού") ON DELETE CASCADE ON UPDATE CASCADE 
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΠΗΓΑΙΝΕΙ (
		"id_οδηγού"	INTEGER NOT NULL,
		"id_σταθμού"	INTEGER NOT NULL,
		FOREIGN KEY("id_οδηγού") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY("id_σταθμού") REFERENCES "ΣΤΑΘΜΟΣ"("id_σταθμού") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("id_οδηγού","id_σταθμού")
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΠΛΗΡΩΜΗ (
		"αριθμός_φόρτισης"	INTEGER NOT NULL,
		"ποσό_πληρωμής"	INTEGER NOT NULL,
		"τρόπος_πληρωμής"	TEXT NOT NULL DEFAULT 'ΜΕΤΡΗΤΑ',
		"αριθμός_κάρτας"	INTEGER,
		FOREIGN KEY("αριθμός_κάρτας") REFERENCES "ΚΑΡΤΑ"("αριθμός_κάρτας") ON DELETE SET NULL ON UPDATE CASCADE,
		FOREIGN KEY("αριθμός_φόρτισης") REFERENCES "ΦΟΡΤΙΣΗ"("αριθμός_φόρτισης") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("αριθμός_φόρτισης" AUTOINCREMENT)
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΡΑΝΤΕΒΟΥ (
		"ώρα_άφιξης"	TEXT NOT NULL,
		"id_οδηγού"	INTEGER NOT NULL,
		"αριθμός_φόρτισης"	INTEGER,
		"αριθμός_ραντεβού"	INTEGER NOT NULL,
		FOREIGN KEY("id_οδηγού") REFERENCES "ΙΔΙΟΚΤΗΤΗΣ"("id") ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY("αριθμός_φόρτισης") REFERENCES "ΦΟΡΤΙΣΗ"("αριθμός_φόρτισης") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("αριθμός_ραντεβού" AUTOINCREMENT)
		);
		''')
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΣΤΑΘΜΟΣ (
		"id_σταθμού"	INTEGER NOT NULL,
		"τηλ_επικοινωνίας"	INTEGER NOT NULL,
		"τόπος"	TEXT NOT NULL,
		"θέσεις_φόρτισης"	INTEGER DEFAULT 1,
		"διεύθυνση"	TEXT NOT NULL,
		PRIMARY KEY("id_σταθμού" AUTOINCREMENT)
		);
		''')	
		self.conn.commit()

		self.conn.execute('''CREATE TABLE ΦΟΡΤΙΣΗ (
		"αριθμός_φόρτισης"	INTEGER NOT NULL,
		"ενέργεια_kWh"	INTEGER,
		"κόστος_φόρτισης"	FLOAT,
		"πινακίδες_αυτοκινήτου"	TEXT,
		"αριθμός_θέσης_φόρτισης"	INTEGER NOT NULL,
		"ώρα_έναρξης"	TEXT,
		"ώρα_λήξης"	TEXT,
		"ημερομηνία_φόρτισης"	TEXT,	
		FOREIGN KEY("αριθμός_θέσης_φόρτισης") REFERENCES "ΘΕΣΗ"("αριθμός_θέσης") ON DELETE CASCADE ON UPDATE CASCADE,
		FOREIGN KEY("πινακίδες_αυτοκινήτου") REFERENCES "ΑΥΤΟΚΙΝΗΤΟ"("πινακίδες") ON DELETE CASCADE ON UPDATE CASCADE,
		PRIMARY KEY("αριθμός_φόρτισης")
		);
		''')
		self.conn.commit()

		self.conn.close()

i1 = Initialisation()