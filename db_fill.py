'''database fill in python'''

import sqlite3 as sql
import datetime
import random
import os

class Fill:
    def __init__(self):

        self.conn = sql.connect("ev.db")
        self.cursor = self.conn.cursor()
        self.fill_db()
        self.conn.close()

    def fill_db(self):
        
        cards_dict = {}
        acc_creation_dict = {}
        time_dict = {}
        plat_dict = {}
        numbers_list = []
        plates_list = []
        locs = []
        addrs = []

        for i in range(1,100):
            first_name, last_name, email, card_name = self.get_names()
            cards_dict[i] = card_name
            tel = self.create_random_tel()
            addr, loc = self.get_locs()
            acc_creation = self.create_random_dates(datetime.date(2020,1,1))
            acc_creation_dict[i] = acc_creation
            acc_creation = acc_creation.strftime("%Y-%m-%d")
            id_data = [first_name, last_name, i, email, int(tel), loc, addr, acc_creation]
            print(id_data)
            self.conn.execute('''INSERT INTO ΙΔΙΟΚΤΗΤΗΣ (όνομα, επίθετο, id, email, τηλ, τόπος, ημ_δημιουργίας_λογαριασμού)VALUES(?,?,?,?,?,?,?)''', (str(first_name), str(last_name), int(i), str(email), int(tel), str(loc), str(acc_creation)))
            self.conn.commit()

        for i in range(1,100):
            brand, model, year = self.get_cars()
            plates = self.create_random_plates()
            plates_list.append(plates)
            car_data = [plates, brand, model, year, i]
            print(car_data)
            self.conn.execute('''INSERT INTO ΑΥΤΟΚΙΝΗΤΟ (πινακίδες, μάρκα, μοντέλο, έτος_κατασκευής, id_οδηγού)VALUES(?,?,?,?,?)''', (str(plates), str(brand), str(model), str(year), int(i)))
            self.conn.commit()

        dr_ids = range(1,100)
        dr_id = random.sample(dr_ids, 20)

        for i in range(1,20):
            number, cvc, exp = self.create_card()
            card_data = [cards_dict[dr_id[i]], number, exp, cvc, dr_id[i]]
            print(card_data)
            self.conn.execute(
                '''INSERT INTO ΚΑΡΤΑ (ονοματεπώνυμο_κατόχου, αριθμός_κάρτας, ημερομηνία_λήξης, CVC, id_κατόχου)VALUES(?,?,?,?,?)''',
                (str(cards_dict[dr_id[i]]), int(number), str(exp), int(cvc), int(dr_id[i])))
            self.conn.commit()

        for i in range(1, 20):
            st_tel = self.create_random_tel()
            st_addr, st_loc = self.get_dist_locs(i-1)
            st_chargers = random.randint(1,5)
            station_data = [i, st_tel, st_loc, st_chargers, st_addr]
            print(station_data)
            self.conn.execute(
                '''INSERT INTO ΣΤΑΘΜΟΣ (id_σταθμού, τηλ_επικοινωνίας, τόπος, θέσεις_φόρτισης, διεύθυνση)VALUES(?,?,?,?,?)''',
                (int(i), int(st_tel), str(st_loc), int(st_chargers), str(st_addr)))
            self.conn.commit()

            kr_ids = range(1, 100)
            kr_id = random.sample(kr_ids, 50)

        for i in range(1, 50):
            stars = self.create_review()
            date = self.create_random_dates(acc_creation_dict[kr_id[i]]).strftime("%Y-%m-%d")
            st_id = random.randint(1, 20)
            review_data = [i, stars, date, kr_id[i], st_id]
            print(review_data)
            self.conn.execute(
                '''INSERT INTO ΚΡΙΤΙΚΗ (id_κριτικής, αστέρια, ημερομηνία_κριτικής, id_οδηγού, id_σταθμού)VALUES(?,?,?,?,?)''',
                (int(i), int(stars), str(date), int(kr_id[i]), int(st_id)))
            self.conn.commit()

        for i in range(1, 20):
            self.cursor.execute("select θέσεις_φόρτισης from ΣΤΑΘΜΟΣ where id_σταθμού = '" + str(i) + "';")
            chargers = self.cursor.fetchone()
            chargers = int(chargers[0])
            if chargers > 1:
                j = 1
                while j <= chargers:
                    number = int(str(i) + str(j))
                    numbers_list.append(number)
                    type, cost, occ = self.create_charger(number)
                    chargers_data = [number, occ, i, type, cost]
                    print(chargers_data)
                    self.conn.execute(
                        '''INSERT INTO ΘΕΣΗ (αριθμός_θέσης, κατειλημμένη, id_σταθμού, τύπος_φορτιστή, χρέωση_ανά_τύπο)VALUES(?,?,?,?,?)''',
                        (int(number), int(occ), int(i), str(type), str(cost)))
                    self.conn.commit()
                    j += 1
            else:
                number = int(str(i) + str(1))
                numbers_list.append(number)
                type, cost, occ = self.create_charger(number)
                chargers_data = [number, occ, i, type, cost]
                print(chargers_data)
                self.conn.execute(
                    '''INSERT INTO ΘΕΣΗ (αριθμός_θέσης, κατειλημμένη, id_σταθμού, τύπος_φορτιστή, χρέωση_ανά_τύπο)VALUES(?,?,?,?,?)''',
                    (int(number), int(occ), int(i), str(type), str(cost)))
                self.conn.commit()

        for i in range(1,80):
            energy, price, plat, num, start, end, date = self.create_charge(plates_list, numbers_list)
            time_dict[i] = start
            plat_dict[i] = plat
            price = float("{:.2f}".format(price))
            if i == 79:
                hour_start = datetime.datetime.today().strftime('%H:%M')
                date = datetime.datetime.today().strftime('%Y-%m-%d')
                charge_data = [i, plat, num, hour_start, date]
                print(charge_data)
                self.conn.execute(
                    '''INSERT INTO ΦΟΡΤΙΣΗ (αριθμός_φόρτισης, πινακίδες_αυτοκινήτου, αριθμός_θέσης_φόρτισης, ώρα_έναρξης, ημερομηνία_φόρτισης)VALUES(?,?,?,?,?)''',
                    (int(i), str(plat), int(num), str(hour_start), str(date)))
                self.conn.commit()
            else:
                charge_data = [i, energy, price, plat, num, start, end, date]
                print(charge_data)
                self.conn.execute(
                    '''INSERT INTO ΦΟΡΤΙΣΗ (αριθμός_φόρτισης, ενέργεια_kWh, κόστος_φόρτισης, πινακίδες_αυτοκινήτου, αριθμός_θέσης_φόρτισης, ώρα_έναρξης, ώρα_λήξης, ημερομηνία_φόρτισης)VALUES(?,?,?,?,?,?,?,?)''',
                    (int(i), int(energy), float(price), str(plat), int(num), str(start), str(end), str(date)))
                self.conn.commit()
                self.update_chargers(numbers_list)
                payment = self.create_payment()
                payment_data = [i, price, payment]
                print(payment_data)
                self.conn.execute(
                    '''INSERT INTO ΠΛΗΡΩΜΗ (αριθμός_φόρτισης, ποσό_πληρωμής, τρόπος_πληρωμής)VALUES(?,?,?)''',
                    (int(i), float(price), str(payment)))
                self.conn.commit()

        ch_ids = range(1, 80)
        ch_id = random.sample(ch_ids, 20)

        for i in range(1, 20):
            r_start = time_dict[ch_id[i]]
            r_plat = plat_dict[ch_id[i]]
            self.cursor.execute("select id_οδηγού from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες = '" + str(r_plat) + "';")
            r_dr_id = self.cursor.fetchone()
            r_dr_id = r_dr_id[0]
            r_data = [r_start, r_dr_id, ch_id[i], i]
            print(r_data)
            self.conn.execute(
                '''INSERT INTO ΡΑΝΤΕΒΟΥ (ώρα_άφιξης, id_οδηγού, αριθμός_φόρτισης, αριθμός_ραντεβού)VALUES(?,?,?,?)''',
                (str(r_start), int(r_dr_id), int(ch_id[i]), int(i)))
            self.conn.commit()

    def update_chargers(self, ch_list):

        for charger in ch_list:
            if not self.check_full_or_empty(charger):
                self.conn.execute("update ΘΕΣΗ set κατειλημμένη = '" + str(1) + "' where αριθμός_θέσης = '" + str(charger) + "';")
                self.conn.commit()

    def create_random_plates(self):

        first_lets = ['ΥΑ', 'ΥΒ', 'ΥΕ', 'ΥΖ', 'ΥΗ', 'ΖΖ', 'ΖΗ', 'ΖΚ', 'ΖΜ', 'ΙΒ', 'ΙΕ', 'ΙΖ', 
                   'ΙΗ', 'ΙΚ', 'ΙΜ', 'ΙΟ', 'ΙΡ', 'ΙΤ', 'ΙΥ', 'ΧΕ', 'ΧΖ', 'ΧΗ', 'ΧΡ', 'ΧΤ', 
                   'ΧΥ', 'ΧΧ', 'ΗΒ', 'ΟΑ', 'ΟΒ', 'ΟΕ', 'ΟΖ', 'ΟΗ', 'ΟΙ', 'ΟΚ', 'ΟΜ', 'ΟΝ', 
                   'ΟΟ', 'ΟΤ', 'ΟΥ', 'ΟΧ', 'ΧΜ', 'ΖΕ', 'ΖI', 'ΖΟ', 'ΥΙ', 'ΥΚ', 'ΥΜ', 'ΥΝ', 
                   'ΖΝ', 'ΖΡ', 'ΒΕ', 'ΒΖ', 'ΒΗ', 'ΒΧ', 'ΤΖ', 'ΥΟ', 'ΥΡ', 'ΥΤ', 'ΖΤ', 'ΒΝ', 
                   'ΒΡ', 'ΥΥ', 'ΥΧ', 'ΖΥ', 'ΖΧ', 'ΒΚ', 'ΒΜ', 'ΜΕ', 'ΑΙ', 'ΤΗ', 'ΑΡ', 'ΤΜ',
                   'ΤΡ', 'ΑΤ', 'ΑΧ', 'ΑΖ', 'ΑΟ', 'ΑΑ', 'ΑΥ', 'ΒΙ', 'ΒΥ', 'ΡΝ', 'ΡΜ', 'ΤΟ',
                   'ΡΟ', 'ΡΚ', 'ΡΥ', 'ΡΧ', 'ΚΧ', 'ΕΑ', 'ΕΒ', 'ΜΧ', 'ΟΡ', 'ΧΑ', 'ΕΗ', 'ΕΙ',
                   'ΚΗ', 'ΖΑ', 'ΖΒ', 'ΗΑ', 'ΗΕ', 'ΗΜ', 'ΗΧ', 'ΗΡ', 'ΗΚ', 'ΗΖ', 'ΗΗ', 'ΗΙ', 
                   'ΗΤ', 'ΗΝ', 'ΝΑ', 'ΝΒ', 'ΝΕ', 'ΝΖ', 'ΝΗ', 'ΝΙ', 'ΝΚ', 'ΝΜ', 'ΝΝ', 'ΝΟ', 
                   'ΝΡ', 'ΝΤ', 'ΝΥ', 'ΝΧ', 'ΙΝ', 'ΙΙ', 'ΚΒ', 'ΑΒ', 'ΚΑ', 'ΜΚ', 'ΚΤ', 'ΚΥ', 
                   'ΕΤ', 'ΤΒ', 'ΤΕ', 'ΚΕ', 'ΚΙ', 'ΕΧ', 'ΚΖ', 'ΜΝ', 'ΚΡ', 'ΡΒ', 'ΕΜ', 'ΕΖ', 
                   'ΕΝ', 'ΕΟ', 'ΑΚ', 'ΜΡ', 'ΡΙ', 'ΡΡ', 'ΡΤ', 'ΑΝ', 'ΑΕ', 'ΜΥ', 'ΜΤ', 'ΜΗ',
                   'ΕΥ', 'ΒΟ', 'ΒΒ', 'ΒΑ', 'ΒΤ', 'ΚΜ', 'ΜΖ', 'ΑΗ' ,'ΗΟ', 'ΕΕ', 'ΜΜ', 'ΚΝ', 
                   'ΤΙ', 'ΡΖ', 'ΤΧ', 'ΡΕ', 'ΡΗ', 'ΚΟ', 'ΚΚ', 'ΤΤ', 'ΜΟ', 'ΜΒ', 'ΕΡ', 'ΙΧ',
                   'ΤΚ', 'ΤΝ', 'ΜΙ', 'ΗΥ', 'ΡΑ', 'ΑΜ', 'ΧΚ', 'ΜΑ', 'ΧΝ', 'ΧΒ', 'ΤΥ', 'ΧΙ',
                   'ΧΟ']
        last_let = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο',
                    'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω']
        first = random.choice(first_lets)
        last = random.choice(last_let)
        letters = [first, last]
        letters = ''.join(letters)

        plates = letters + ' ' + ''.join(str(random.randint(0, 9)) for _ in range(4))

        return plates 

    def create_random_dates(self, start_date):

        now = datetime.date.today()
        days = now - start_date
        days = days.days
        rand_days = random.randrange(days)
        date = start_date + datetime.timedelta(days = rand_days)

        return date

    def create_random_tel(self):

        tel = '69'+''.join(str(random.randint(0, 9)) for _ in range(8))

        return tel

    def get_names(self):
        
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        names = open(os.path.join(__location__, 'full_names.txt')).read().splitlines()
        full_name = random.choice(names)
        full_name = full_name.split()
        first_name = full_name[0]
        last_name = full_name[-1]
        email = (first_name + last_name + "gmail.com").lower()
        card_name = first_name[0] + ' ' + last_name

        return first_name, last_name, email, card_name

    def create_card(self):
        
        card_number = "4" + ''.join(str(random.randint(0, 9)) for _ in range(15))
        cvc = ''.join(str(random.randint(0, 9)) for _ in range(3))
        
        end = datetime.date(2028,1,1)
        start_date = datetime.date.today()
        days = end - start_date
        days = days.days
        rand_days = random.randrange(days)
        exp_date = start_date + datetime.timedelta(days = rand_days)
        exp_date = str(exp_date.year) + '-' + str(exp_date.month)

        return card_number, cvc, exp_date

    def create_review(self):

        stars = random.randint(1,5)

        return stars

    def create_payment(self):

        methods = ['ΜΕΤΡΗΤΑ', 'ΚΑΡΤΑ']
        method_of_paym = random.choice(methods)

        return method_of_paym

    def get_cars(self):
        
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        cars = open(os.path.join(__location__, 'cars.txt')).read().splitlines()
        car = random.choice(cars)
        car = car.split()
        brand = car[0]
        model = ' '.join(car[1:])
        years = ['2020', '2021', '2022', '2023', '2024']
        year = random.choice(years)

        return brand, model, year

    def get_locs(self):

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        locs = open(os.path.join(__location__, 'stations.txt')).read().splitlines()
        location = random.choice(locs)
        locs.remove(location)
        location = location.split(", ")
        addr = location[0]
        loc = location[1][0:-7]
        return addr, loc

    def get_dist_locs(self, i):

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        locs = open(os.path.join(__location__, 'stations.txt')).read().splitlines()
        location = locs[i]
        location = location.split(", ")
        addr = location[0]
        loc = location[1][0:-7]
        return addr, loc

    def create_charge(self, plates, nums):

        #αριθμός_φόρτισης, ενέργεια_kWh, κόστος_φόρτισης, πινακίδες_αυτοκινήτου, αριθμός_θέσης_φόρτισης, ώρα_έναρξης, ώρα_λήξης, ημερομηνία_φόρτισης
        plat = random.choice(plates)
        num = random.choice(nums)
        self.cursor.execute("select τύπος_φορτιστή from ΘΕΣΗ where αριθμός_θέσης = '" + str(num) + "';")
        type = self.cursor.fetchone()
        if type[0] == "ac":
            cost = 0.5
        elif type[0] == "dc":
            cost = 0.65
        energy = random.randint(10, 60)
        price = energy*cost

        start = datetime.datetime(2024, 1, 12,7,00)
        start = start + datetime.timedelta(hours=random.randrange(12), minutes=random.randrange(60))
        end = start + datetime.timedelta(hours=random.randint(1,8), minutes=random.randrange(60))
        start = start.strftime("%H:%M")
        end = end.strftime("%H:%M")
        date = self.create_random_dates(datetime.date(2020,1,1))
        date = date.strftime("%Y-%m-%d")

        return energy, price, plat, num, start, end, date


    def create_charger(self, charger):

        types = ["ac", "dc"]
        type = random.choice(types)
        if type == "ac":
            cost = 0.5
        elif type == "dc":
            cost = 0.65
        if self.check_full_or_empty(charger):
            return type, cost, 0
        else:
            return type, cost, 1

    def check_full_or_empty(self, charger):

        self.cursor.execute("select αριθμός_θέσης_φόρτισης from ΦΟΡΤΙΣΗ where ώρα_λήξης is NULL")
        occ_chargers = self.cursor.fetchall()
        if occ_chargers:
            if charger in occ_chargers[0]:
                return False
            return True
        else:
            return True

f1 = Fill()