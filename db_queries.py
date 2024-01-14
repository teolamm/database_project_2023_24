import sqlite3 as sql

class Queries:

    def __init__(self):

        self.conn = sql.connect('ev.db')
        self.cursor = self.conn.cursor()
        self.queries()
        self.conn.close()

    def queries(self):

        print("\nlist of all the drivers living in Athens:")
        ath = "Athens"
        self.cursor.execute("select όνομα, επίθετο from ΙΔΙΟΚΤΗΤΗΣ where τόπος = '" + str(ath) + "';")
        drivers = self.cursor.fetchall()
        for driver in drivers:
            print(driver[0], driver[1])

        print("\nlist with all cities having an ev recharge station:")
        self.cursor.execute('''select distinct τόπος from ΣΤΑΘΜΟΣ order by τόπος''')
        locs = self.cursor.fetchall()
        for loc in locs:
            print(loc[0])

        print("\nlist of every station and its average review: ")
        self.cursor.execute('''select avg(αστέρια), id_σταθμού, τόπος, διεύθυνση
                                from ΚΡΙΤΙΚΗ natural join ΣΤΑΘΜΟΣ
                                group by id_σταθμού
                                having avg(αστέρια)>0''')
        stars = self.cursor.fetchall()
        for st in stars:
            print("station id:", st[1], "at: ", st[2] + ",", st[3], "average review: {:.2f} stars".format(st[0]))

        print("\nlist of all stations with dc chargers: ")
        self.cursor.execute('''select distinct id_σταθμού, τόπος, διεύθυνση
                                from ΣΤΑΘΜΟΣ natural join ΘΕΣΗ
                                where τύπος_φορτιστή = "dc"
                            ''')
        fast = self.cursor.fetchall()
        for f in fast:
            print("station id:", f[0], "at: ", f[1] + ",", f[2])

        print("\nlist of every driver and total energy of all their charges: ")
        self.cursor.execute('''select  id_οδηγού, πινακίδες, sum(ενέργεια_kWh)
                                from ΦΟΡΤΙΣΗ join ΑΥΤΟΚΙΝΗΤΟ on πινακίδες = πινακίδες_αυτοκινήτου
                                group by id_οδηγού
                                having sum(ενέργεια_kWh) > 1
                                order by id_οδηγού asc
                                ''')
        energy = self.cursor.fetchall()
        for e in energy:
            print("driver's id:", e[0], "- car's plates:", e[1], "- total energy consumption:", e[2])

        print("\nlist of all the Teslas and their construction years: ")
        self.cursor.execute('''select μοντέλο, έτος_κατασκευής
                                from ΑΥΤΟΚΙΝΗΤΟ
                                where μάρκα = 'Tesla'
                                ''')
        teslas = self.cursor.fetchall()
        for tesla in teslas:
            print(tesla[0], "-", tesla[1])

        self.cursor.execute('''select max(αριθμός_ραντεβού), max(αριθμός_φόρτισης),  100 * cast(max(αριθμός_ραντεβού) as decimal(2,2)) / cast(max(αριθμός_φόρτισης) as decimal(2,2))
                                from ΡΑΝΤΕΒΟΥ natural join ΦΟΡΤΙΣΗ
                                ''')
        stat = self.cursor.fetchone()
        print("\nnumber of appointments: " + str(stat[0]) + "\nnumber of charges: " + str(stat[1]) + "\npercentage of charges happening after an appointment: " + str(stat[2]) + "%")

        print("\nlist of available chargers per station: ")
        self.cursor.execute('''select id_σταθμού, count(*)
                                from ΣΤΑΘΜΟΣ natural join ΘΕΣΗ
                                where κατειλημμένη = 0
                                group by id_σταθμού
                                having count(*)>1
                                order by id_σταθμού
                            ''')
        free_chargers = self.cursor.fetchall()
        for ch in free_chargers:
            print("station id:",ch[0], "- free spots: ", ch[1])

q1 = Queries()