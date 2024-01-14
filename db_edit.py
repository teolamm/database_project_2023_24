import sqlite3 as sql
import datetime
import functools
import re

class Edit:

    def __init__(self):

        self.conn = sql.connect("ev.db")
        self.cursor = self.conn.cursor()

        print("\n1 - driver\n2 - car\n3 - appointments\n4 - stations\n5 - cards\n6 - exit")
        num = input("\nchoose mode: ")
        if num == '1':
            print("\n1 - insert driver\n2 - delete driver\n3 - edit driver\n4 - go back")
            dr = input("\nchoose mode: ")
            if dr == '1':
                self.new_driver()
            elif dr == '2':
                del_id = int(input("give your id: "))
                self.del_driver(del_id)
            elif dr == '3':
                edit_id = int(input("give your id: "))
                self.edit_driver(edit_id)
            elif dr == '4':
                self.__init__()
                
        elif num == '2':
            drivers_id = int(input("give your id: "))

            self.cursor.execute("select id from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(drivers_id) + "';")
            result = self.cursor.fetchone()
            if result:
                i = 1
                self.cursor.execute("select πινακίδες from ΑΥΤΟΚΙΝΗΤΟ where id_οδηγού = '" + str(drivers_id) + "';")
                cars = self.cursor.fetchall()
                if len(cars) > 1:
                    print("\nyour cars have the following plates: ")
                    for car in cars:
                        print(i, ' - ', car[0])
                        i += 1
                elif len(cars) == 1:
                    print("your card is: ", cars[0][0])
                else:
                    print("\nno car has been inserted...")
                    print("\n1 - insert car\n2 - go back")
                    n_car = input("\nchoose mode: ")
                    if n_car == '1':
                        self.new_car(drivers_id)
                    elif n_car == '2':
                        self.__init__()
                    else:
                        print("\ninvalid input...")
                        self.__init__()
                print("\n1 - insert car\n2 - delete car\n3 - edit car\n4 - view detals\n5 - go back")
                car = input("\nchoose mode: ")
                if car == '1':
                    self.new_car(drivers_id)
                elif car == '2':
                    self.del_car(drivers_id)
                elif car == '3':
                    self.edit_car(drivers_id)
                elif car == '4':
                    self.view_car(cars)
                elif car == '5':
                    self.__init__()
                else:
                    print("\ninvalid input")
                    self.__init__()
            else:
                print("\nthis id does not exist...")
                self.__init__()
        
        elif num == '3':
            #self.turn_appointment_into_charge()
            drivers_id = int(input("give your id: "))
            self.cursor.execute("select id from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(drivers_id) + "';")
            result = self.cursor.fetchone()
            if result:
                i = 1
                self.cursor.execute(
                    "select * from ΡΑΝΤΕΒΟΥ natural join ΦΟΡΤΙΣΗ where id_οδηγού = '" + str(drivers_id) + "' and αριθμός_φόρτισης in (select αριθμός_φόρτισης from ΦΟΡΤΙΣΗ where ώρα_έναρξης is null and ώρα_λήξης is null);")
                apps = self.cursor.fetchall()
                if apps:
                    print("\nyour appointments are:")
                    for app in apps:
                        charger = app[-4]
                        charger = str(charger)
                        station = charger[0:-2]
                        self.cursor.execute("select διεύθυνση, τόπος from ΣΤΑΘΜΟΣ where id_σταθμού = '" + str(station) + "';")
                        loc = self.cursor.fetchone()
                        print(i,
                              ' - appointment number: ' + str(app[2]) + ', date: ' + app[-1] + ', at: ' + app[0] + ', in: ' + loc[1] + ', ' + loc[0] + ', at charger: ' + charger + '')
                        i += 1
                else:
                    print("\nyou have not booked any appointments...")
                    print("\n1 - insert new appointment\n2 - go back")
                    app = input("choose mode: ")
                    if app == '1':
                        self.new_app(drivers_id)
                    elif app == '2':
                        self.__init__()
                    else:
                        print("\ninvalid input...")
                        self.__init__()
                print("\n1 - insert new appointment\n2 - delete appointment\n3 - edit appointment\n4 - go back")
                app = input("\nchoose mode: ")
                if app == '1':
                    self.new_app(drivers_id)
                elif app == '2':
                    self.del_app(drivers_id)
                elif app == '3':
                    self.edit_app(drivers_id)
                elif app == '4':
                    self.__init__()
                else:
                    print("\ninvalid input")
                    self.__init__()
            else:
                print("\nthis id does not exist...")
                self.__init__()

        elif num == '4':
            print("\n1 - view all stations\n2 - search for nearby stations\n3 - go back")
            station = input("\nchoose mode: ")
            if station == '1':
                length = self.view_stations()
                self.__init__()
            if station == '2':
                loc = input("enter the location where you want to search for nearby stations: ")
                loc = self.locs_edit(loc)
                ex = self.check_nearby(loc)
                if ex:
                    length = self.view_stations(loc)
                    self.__init__()
                else:
                    print("no nearby stations found")
                    self.__init__()
            elif station == '3':
                self.__init__()
            else:
                print("\ninvalid input...")
                self.__init__()

        elif num == '5':
            drivers_id = int(input("give your id: "))
            self.cursor.execute("select id from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(drivers_id) + "';")
            result = self.cursor.fetchone()
            if result:
                i = 1
                self.cursor.execute("select αριθμός_κάρτας from ΚΑΡΤΑ where id_κατόχου = '" + str(drivers_id) + "';")
                cards = self.cursor.fetchall()
                if len(cards) > 1:
                    print("\nyour cards have the following numbers: ")
                    for card in cards:
                        print(i, ' - ', card[0])
                        i += 1
                elif len(cards) == 1:
                    print("your card is: ", cards[0][0])
                else:
                    print("\nno card has been inserted...")
                    print("\n1 - insert card\n2 - go back")
                    n_card = input("\nchoose mode: ")
                    if n_card == '1':
                        self.new_card(drivers_id)
                    elif n_card == '2':
                        self.__init__()
                    else:
                        print("\ninvalid input...")
                        self.__init__()
                print("\n1 - insert card\n2 - delete card\n3 - view details\n4 - go back")
                card = input("\nchoose mode: ")
                if card == '1':
                    self.new_card(drivers_id)
                elif card == '2':
                    self.del_card(drivers_id)
                elif card == '3':
                    self.view_card(cards)
                elif card == '4':
                    self.__init__()
                else:
                    print("\ninvalid input")
                    self.__init__()
            else:
                print("\nthis id does not exist...")
                self.__init__()

        elif num == '6':
            self.exit()

        else:
            print("\ninvalid input...")
            self.__init__()

    def new_driver(self):

        name = input("give full name: ")
        if self.check_name(name):
            name = name.split()
            fname = name[0]
            lname = name[1]
            email = input("give your email: ")
            if self.check_email(email):
                tel = input("give your telephone number: ")
                if self.check_phone_num(tel):
                    loc = input("give your location: ")
                    if loc.isalpha():
                        acc_creation = datetime.datetime.now().strftime("%Y-%m-%d")
                        self.cursor.execute("SELECT max(id) FROM ΙΔΙΟΚΤΗΤΗΣ;")
                        driver_id = self.cursor.fetchone()
                        driver_id = functools.reduce(lambda sub, ele: sub * 10 + ele, driver_id)
                        driver_id = driver_id + 1

                        self.conn.execute(
                            '''INSERT INTO ΙΔΙΟΚΤΗΤΗΣ (όνομα, επίθετο, id, email, τηλ, τόπος, ημ_δημιουργίας_λογαριασμού)VALUES(?,?,?,?,?,?,?)''',
                            (str(fname), str(lname), int(driver_id), str(email), int(tel), str(loc), str(acc_creation)))
                        self.conn.commit()
                        print("\nnew driver inserted successfully\nyour id is: ", driver_id)
                    else:
                        print("\ninvalid location...")
                    self.__init__()
                else:
                    print("\ninvalid phone number...")
                    self.__init__()
            else:
                print("\ninvalid email address...")
                self.__init__()
        else:
            print("\ninvalid full name...")
            self.__init__()

    def del_driver(self, del_id):

        self.cursor.execute("select id from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(del_id) + "';")
        result = self.cursor.fetchone()
        if result:
            sure = input("\nare you sure you want to delete this driver (y - n)? ")
            if sure == "y":
                self.conn.execute("delete from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(del_id) + "';")
                self.conn.commit()
                print("\nsuccessfully deleted driver")
            elif sure == "n":
                print("\ndriver was not deleted")
            else:
                print("\ninvalid input...")
            self.__init__()
        else:
            print("\nthis is does not exist...")
            self.__init__()


    def edit_driver(self, edit_id):

        self.cursor.execute("select id from ΙΔΙΟΚΤΗΤΗΣ where id = '" + str(edit_id) + "';")
        result = self.cursor.fetchone()
        if result:
            ed = int(input("which attribute do you want to update?\n1 - name\n2 - email\n3 - telephone\n4 - location\n"))
            if ed == 1:
                new_name = input("give new name: ")
                if self.check_name(new_name):
                    new_name = new_name.split()
                    fname = new_name[0]
                    lname = new_name[1]
                    self.conn.execute(
                        "UPDATE ΙΔΙΟΚΤΗΤΗΣ SET όνομα = '" + str(fname) + "'  where id = '" + str(edit_id) + "';")
                    self.conn.commit()
                    self.conn.execute(
                        "UPDATE ΙΔΙΟΚΤΗΤΗΣ SET επίθετο = '" + str(lname) + "' where id = '" + str(edit_id) + "';")
                    self.conn.commit()
                    edit = input("would you like to keep editing the same driver (y or n)? ")
                    if edit == 'y':
                        self.edit_driver(edit_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited driver")
                        self.__init__()
                    else:
                        print("\ninvalid")
                        self.__init__()
                else:
                    print("\ninvalid name...")
                    self.__init__()
            elif ed == 2:
                new_email = input("give new email: ")
                if self.check_email(new_email):
                    self.conn.execute("UPDATE ΙΔΙΟΚΤΗΤΗΣ SET email = '" + str(new_email) + "' where id = '" + str(edit_id) + "';")
                    self.conn.commit()
                    edit = input("would you like to keep editing the same driver (y or n)? ")
                    if edit == 'y':
                        self.edit_driver(edit_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited driver")
                        self.__init__()
                    else:
                        print("\ninvalid")
                        self.__init__()
                else:
                    print("\ninvalid email")
                    self.__init__()
            elif ed == 3:
                new_tel = input("give new telephone: ")
                if self.check_phone_num(new_tel):
                    self.conn.execute("UPDATE ΙΔΙΟΚΤΗΤΗΣ SET τηλ = '" + int(new_tel) + "' where id = '" + str(edit_id) + "';")
                    self.conn.commit()
                    edit = input("would you like to keep editing the same driver (y or n)? ")
                    if edit == 'y':
                        self.edit_driver(edit_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited driver")
                        self.__init__()
                    else:
                        print("\ninvalid")
                        self.__init__()
                else:
                    print("\ninvalid phone number...")
                    self.__init__()
            elif ed == 4:
                new_loc = input("give new location: ")
                if new_loc.isalpha():
                    self.conn.execute("UPDATE ΙΔΙΟΚΤΗΤΗΣ SET τόπος = '" + str(new_loc) + "' where id = '" + str(edit_id) + "';")
                    self.conn.commit()
                    edit = input("\nwould you like to keep editing the same driver?(y or n)")
                    if edit == 'y':
                        self.edit_driver(edit_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited driver")
                        self.__init__()
                    else:
                        print("\ninvalid")
                        self.__init__()
                else:
                    print("\ninvalid location")
                    self.__init__()
            else:
                print("\ninvalid input...")
                self.__init__()
        else:
            print("\nthis is does not exist...")
            self.__init__()

        print("\nsuccessfully edited driver")
        self.__init__()

    def new_car(self, drivers_id):

        drivers_id = int(drivers_id)
        plates = input("give plates: ")
        if self.check_plates(plates):
            plates = plates.upper()
            self.cursor.execute("select πινακίδες from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες =  '" + str(plates) + "';")
            unique = self.cursor.fetchone()
            if not unique:
                brand = input("give brand: ")
                model = input("give model: ")
                year = input("give construction year: ")
                if self.check_year(year):
                    self.conn.execute(
                        '''INSERT INTO ΑΥΤΟΚΙΝΗΤΟ (πινακίδες, μάρκα, μοντέλο, έτος_κατασκευής, id_οδηγού)VALUES(?,?,?,?,?)''',
                        (str(plates), str(brand), str(model), str(year), int(drivers_id)))
                    self.conn.commit()
                    print("new car inserted successfully\n")
                    self.__init__()
                else:
                    print("\ninvalid input for year...")
                    self.__init__()
            else:
                print("\nthese plates already exist in another car...")
                self.__init__()
        else:
            print("\ninvalid plates...")
            self.__init__()

    def edit_car(self, drivers_id):

        plates = input("give the plates of the car you want to edit: ")
        if self.check_plates(plates):
            plates = plates.upper()
            self.cursor.execute("select πινακίδες from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες = '" + str(plates) + "';")
            result2 = self.cursor.fetchone()
            if result2:
                c_ed = input(
                    "which attribute do you want to update?\n1 - brand\n2 - model\n3 - year of construction\n")
                if c_ed == '1':
                    new_brand = input("give new brand: ")
                    self.conn.execute(
                        "UPDATE ΑΥΤΟΚΙΝΗΤΟ SET μάρκα = '" + str(new_brand) + "' where id_οδηγού = '" + str(drivers_id) + "' and πινακίδες = '" + str(plates) + "';")
                    self.conn.commit()
                    edit = input("would you like to keep editing the same car (y or n)? ")
                    if edit == 'y':
                        self.edit_car(drivers_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited car")
                        self.__init__()
                    else:
                        print("\ninvalid")
                        self.__init__()
                elif c_ed == '2':
                    new_model = input("give new model: ")
                    self.conn.execute(
                        "UPDATE ΑΥΤΟΚΙΝΗΤΟ SET μοντέλο = '" + str(new_model) + "' where id_οδηγού = '" + str(drivers_id) + "' and πινακίδες = '" + str(plates) + "';")
                    self.conn.commit()
                    edit = input("would you like to keep editing the same car (y or n)? ")
                    if edit == 'y':
                        self.edit_car(drivers_id)
                    elif edit == 'n':
                        print("\nsuccessfully edited car")
                        self.__init__()
                    else:
                        print("invalid")
                        self.__init__()
                elif c_ed == '3':
                    new_year = input("give new year of construction: ")
                    if self.check_year(new_year):
                        self.conn.execute(
                            "UPDATE ΑΥΤΟΚΙΝΗΤΟ SET έτος_κατασκευής = '" + str(new_year) + "' where id_οδηγού = '" + str(drivers_id) + "' and πινακίδες = '" + str(plates) + "';")
                        self.conn.commit()
                        edit = input("would you like to keep editing the same car (y or n)? ")
                        if edit == 'y':
                            self.edit_car(drivers_id)
                        elif edit == 'n':
                            print("\nsuccessfully edited car")
                            self.__init__()
                        else:
                            print("\ninvalid input")
                            self.__init__()
                    else:
                        print("\ninvalid input for year...")
                        self.__init__()
                else:
                    print("invalid input...")
                    self.__init__()
            else:
                print("\na car with these plates does not exist...")
                self.__init__()
        else:
            print("\ninvalid plates...")
            self.__init__()

        print("\nsuccessfully edited car")
        self.__init__()

    def del_car(self, drivers_id):

        plates = input("give the plates of the car you want to delete: ")
        if self.check_plates(plates):
            plates = plates.upper()
            self.cursor.execute("select * from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες = '" + str(plates) + "';")
            result2 = self.cursor.fetchone()
            if result2:
                c_sure = input("\nare you sure you want to delete this car (y - n)? ")
                if c_sure == "y":
                    self.conn.execute("delete from ΑΥΤΟΚΙΝΗΤΟ where id_οδηγού = '" + str(drivers_id) + "' and πινακίδες = '" + str(plates) + "';")
                    self.conn.commit()
                    print("\nsuccessfully deleted car")
                elif c_sure == "n":
                    print("\ncar was not deleted")
                else:
                    print("\ninvalid input...")
                self.__init__()
            else:
                print("a car with these plates does not exist...\n")
                self.__init__()
        else:
            print("\ninvalid plates...")
            self.__init__()

        print("successfully deleted car")
        self.__init__()

    def view_car(self, cars):

        i = 1
        if len(cars) > 1:
            for car in cars:
                print(i, ' - ', car[0])
                i += 1
            choice = input("\nwhich car's details do you want to see (b to go back)? ")
            if choice == 'b':
                self.__init__()
            elif not choice.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                choice = int(choice)
                if choice > len(cars):
                    print("\ninvalid input...")
                    self.__init__()
                else:
                    self.cursor.execute("select * from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες = '" + str(cars[choice-1][0]) + "';")
                    info = self.cursor.fetchone()
                    print("plates: " + info[0] + "\nbrand: " + info[1] + "\nmodel: " + info[2] + "\nconstruction date: " + info[3] + "")
                    self.__init__()

        elif len(cars) == 1:
            self.cursor.execute("select * from ΑΥΤΟΚΙΝΗΤΟ where πινακίδες = '" + str(cars[0][0]) + "';")
            info = self.cursor.fetchone()
            print("plates: " + info[0] + "\nbrand: " + info[1] + "\nmodel: " + info[2] + "\nconstruction date: " + info[
                3] + "")
            self.__init__()

    def new_app(self, id):

        print("\nchoose in which station you want to charge your ev: ")
        print("\n1 - view all stations\n2 - search for nearby stations\n3 - go back")
        stat = input("\nchoose mode: ")
        if stat == '1':
            length = self.view_stations()
            st = input("\nchoose in which station you want to charge your ev (b to go back): ")
            if st == 'b':
                self.__init__()
            elif not st.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                st = int(st)
                if st >= int(length):
                    print("\ninvalid input...")
                    self.__init__()
                else:
                    self.cursor.execute("select id_σταθμού from ΣΤΑΘΜΟΣ")
                    stations = self.cursor.fetchall()
                    chosen_st = stations[st-1][0]
                    charger = self.find_free_chargers(chosen_st)
                    if charger is None:
                        print("\nthis station is full, perhaps you can try another one...")
                        self.__init__()
        elif stat == '2':
            loc = input("enter the location where you want to search for nearby stations: ")
            loc = self.locs_edit(loc)
            ex = self.check_nearby(loc)
            if ex:
                length = self.view_stations(loc)
                if length > 2:
                    st = input("\nchoose in which station you want to charge your ev (b for back): ")
                    if st == 'b':
                        self.__init__()
                    elif not st.isdigit():
                        print("\ninvalid input...")
                        self.__init__()
                    else:
                        st = int(st)-1
                        self.cursor.execute("select id_σταθμού from ΣΤΑΘΜΟΣ where τόπος = '" + str(loc) + "';")
                        stations = self.cursor.fetchall()
                        chosen_st = stations[st][0]
                        charger = self.find_free_chargers(chosen_st)
                        if charger is None:
                            print("\nthis station is full, perhaps you can try another one...")
                            self.__init__()
                elif length == 2:
                    self.cursor.execute("select id_σταθμού from ΣΤΑΘΜΟΣ where τόπος = '" + str(loc) + "';")
                    station = self.cursor.fetchone()
                    chosen_st = station[0]
                    charger = self.find_free_chargers(chosen_st)
                    if charger is None:
                        print("\nthis station is full, perhaps you can try another one...")
                        self.__init__()
            else:
                print("no nearby stations found")
                self.new_app(id)
        elif stat == '3':
            self.__init__()
        else:
            print("\ninvalid input...")
            self.__init__()
        r_date = input("which day do you want to charge your electric vehicle (year-month-day)? ")
        if self.check_date(r_date):
            r_time = input("what time do you want to charge your electric vehicle (hour:minute - you cannot make an appointment before 8:00 or after 20:59)? ")
            if self.check_time(r_time):
                self.cursor.execute("SELECT max(αριθμός_ραντεβού) FROM ΡΑΝΤΕΒΟΥ;")
                r_id = self.cursor.fetchone()
                r_id = r_id[0]
                r_id = r_id + 1
                self.cursor.execute("SELECT max(αριθμός_φόρτισης) FROM ΦΟΡΤΙΣΗ;")
                ch_id = self.cursor.fetchone()
                ch_id = ch_id[0]
                ch_id = ch_id + 1
                self.conn.execute(
                    '''INSERT INTO ΦΟΡΤΙΣΗ (αριθμός_φόρτισης, αριθμός_θέσης_φόρτισης, ημερομηνία_φόρτισης)VALUES(?,?,?)''',
                    (int(ch_id), int(charger), str(r_date)))
                self.conn.commit()
                self.conn.execute(
                    '''INSERT INTO ΡΑΝΤΕΒΟΥ (ώρα_άφιξης, id_οδηγού, αριθμός_φόρτισης, αριθμός_ραντεβού)VALUES(?,?,?,?)''',
                    (str(r_time), int(id), int(ch_id), int(r_id)))
                self.conn.commit()
                print("\nnew appointment inserted successfully\nnew appointment id is: " + str(r_id) + ", date: " + r_date + ", time:" + r_time + " and the charger you are going to use is: " + str(charger) + ".")
                self.__init__()
            else:
                print("\ninvalid time...")
                self.__init__()
        else:
            print("\ninvalid date...")
            self.__init__()

    def del_app(self, id):

        self.cursor.execute("select * from ΡΑΝΤΕΒΟΥ natural join ΦΟΡΤΙΣΗ where id_οδηγού = '" + str(id) + "' and αριθμός_φόρτισης in (select αριθμός_φόρτισης from ΦΟΡΤΙΣΗ where ώρα_έναρξης is null and ώρα_λήξης is null);")
        apps = self.cursor.fetchall()
        if len(apps) > 1:
            choice = input("which appointment do you want to delete (n for none)? ")
            if choice == 'n':
                self.__init__()
            elif not choice.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                choice = int(choice)
                if choice > len(apps):
                    print("\ninvalid input...")
                    self.del_app(id)
                else:
                    self.conn.execute(
                        "delete from ΡΑΝΤΕΒΟΥ where αριθμός_ραντεβού = '" + str(apps[choice-1][3]) + "';")
                    self.conn.commit()
                    self.conn.execute("delete from ΦΟΡΤΙΣΗ where αριθμός_φόρτισης = '" + str(apps[choice-1][2]) + "';")
                    self.conn.commit()
                    print("\nsuccessfully deleted appointment")
                    self.__init__()
        elif len(apps) == 1:
            choice = input("do you want to delete your appointment (y - n)? ")
            if choice == 'y':
                self.conn.execute(
                    "delete from ΡΑΝΤΕΒΟΥ where αριθμός_ραντεβού = '" + str(apps[0][3]) + "';")
                self.conn.commit()
                self.conn.execute("delete from ΦΟΡΤΙΣΗ where αριθμός_φόρτισης = '" + str(apps[0][2]) + "'")
                self.conn.commit()
                print("\nsuccessfully deleted appointment")
                self.__init__()
            elif c_sure == 'n':
                print("\nappointment was not deleted")
            else:
                print("\ninvalid input...")
            self.__init__()
        else:
            print("\nyou have not booked any appointments...")
            self.__init__()

    def edit_app(self, id):

        self.cursor.execute("select * from ΡΑΝΤΕΒΟΥ natural join ΦΟΡΤΙΣΗ where id_οδηγού = '" + str(
            id) + "' and αριθμός_φόρτισης in (select αριθμός_φόρτισης from ΦΟΡΤΙΣΗ where ώρα_έναρξης is null and ώρα_λήξης is null);")
        apps = self.cursor.fetchall()
        if len(apps) > 1:
            choice = input("which appointment do you want to edit (n for none)? ")
            if choice == 'n':
                self.__init__()
            elif not choice.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                choice = int(choice)
                if choice > len(apps):
                    print("\ninvalid input...")
                    self.edit_app(id)
                else:
                    app_ed = input(
                        "which attribute do you want to update?\n1 - date\n2 - time\n3 - go back")
                    if app_ed == '1':
                        n_date = input("give a new date for the appointment (year-month-day): ")
                        if self.check_date(n_date):
                            self.conn.execute("update ΦΟΡΤΙΣΗ set ημερομηνία_φόρτισης = '" + str(n_date) + "' where αριθμός_φόρτισης = '" + str(apps[choice - 1][2]) + "'")
                            self.conn.commit()
                            print("\nsuccessfully edited appointment")
                            self.__init__()
                        else:
                            print("\ninvalid date...")
                            self.__init__()
                    elif app_ed == '2':
                        n_time = input("give a new time for the appointment (hour:minutes -  you cannot make an appointment before 8:00 or after 20:59):")
                        if self.check_time(n_time):
                            self.conn.execute("update RANTEBOY set ώρα_άφιξης = '" + str(
                                n_time) + "' where αριθμός_φόρτισης = '" + str(apps[choice - 1][3]) + "'")
                            self.conn.commit()
                            print("\nsuccessfully edited appointment")
                            self.__init__()
                        else:
                            print("\ninvalid time")
                            self.__init__()
                    elif app_ed == '3':
                        self.__init__()
                    else:
                        print("\ninvalid input...")
                        self.__init__()
        elif len(apps) == 1:
            app_ed = input(
                "which attribute do you want to update?\n1 - date\n2 - time\n3 - go back")
            if app_ed == '1':
                n_date = input("give a new date for the appointment (year-month-day): ")
                if self.check_date(n_date):
                    self.conn.execute("update ΦΟΡΤΙΣΗ set ημερομηνία_φόρτισης = '" + str(
                        n_date) + "' where αριθμός_φόρτισης = '" + str(apps[0][2]) + "'")
                    self.conn.commit()
                    print("\nsuccessfully edited appointment")
                    self.__init__()
                else:
                    print("\ninvalid date...")
                    self.__init__()
            elif app_ed == '2':
                n_time = input(
                    "give a new time for the appointment (hour:minutes -  you cannot make an appointment before 8:00 or after 20:59):")
                if self.check_time(n_time):
                    self.conn.execute("update RANTEBOY set ώρα_άφιξης = '" + str(
                        n_time) + "' where αριθμός_φόρτισης = '" + str(apps[0][3]) + "'")
                    self.conn.commit()
                    print("\nsuccessfully edited appointment")
                    self.__init__()
                else:
                    print("\ninvalid time")
                    self.__init__()
            elif app_ed == '3':
                self.__init__()
            else:
                print("\ninvalid input...")
                self.__init__()
        else:
            print("\nyou have not booked any appointments...")
            self.__init__()

    def new_card(self, id):

        c_name = input("full name in card: ")
        if self.check_name(c_name):
            c_number = input("number: ")
            self.cursor.execute("select * from ΚΑΡΤΑ where αριθμός_κάρτας = '" + str(c_number) + "';")
            double = self.cursor.fetchone()
            if double:
                print("\ncard already exists...")
                self.__init__()
            else:
                if self.check_card_num(c_number):
                    c_exp_month = input("expiration month: ")
                    c_exp_year = input("expiration year: ")
                    if self.check_card_exp(c_exp_year, c_exp_month):
                        c_exp = '-'.join([c_exp_year, c_exp_month])
                        cvc = input("cvc: ")
                        if cvc.isdigit() and len(cvc) == 3:
                            self.conn.execute(
                                '''INSERT INTO ΚΑΡΤΑ (ονοματεπώνυμο_κατόχου, αριθμός_κάρτας, ημερομηνία_λήξης, CVC, id_κατόχου)VALUES(?,?,?,?,?)''',
                                (str(c_name), int(c_number), str(c_exp), int(cvc), int(id)))
                            self.conn.commit()
                            print("\nsuccessfully inserted card")
                            self.__init__()
                        else:
                            print("\ninvalid cvc...")
                            self.__init__()
                    else:
                        print("\ninvalid expiration date...")
                        self.__init__()
                else:
                    print("\ninvalid card number...")
                    self.__init__()
        else:
            print("\ninvalid name...")
            self.__init__()

    def del_card(self, id):

        self.cursor.execute("select αριθμός_κάρτας from ΚΑΡΤΑ where id_κατόχου = '" + str(id) + "';")
        cards = self.cursor.fetchall()
        if len(cards) > 1:
            choice = input("which one do you want to delete (n for none)? ")
            if choice == 'n':
                print("\nno cards were deleted")
                self.__init__()
            elif not choice.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                choice = int(choice)
                if choice > len(cards):
                    print("\ninvalid card...")
                    self.del_card(id)
                else:
                    self.conn.execute(
                        "delete from ΚΑΡΤΑ where αριθμός_κάρτας = '" + str(cards[choice-1][0]) + "';")
                    self.conn.commit()
                    print("\nsuccessfully deleted card")
                    self.__init__()
        elif len(cards) == 1:
            choice = input("do you want to delete your card (y - n)? ")
            if choice == 'y':
                self.conn.execute(
                    "delete from ΚΑΡΤΑ where αριθμός_κάρτας = '" + str(cards[0][0]) + "';")
                self.conn.commit()
                print("\nsuccessfully deleted card")
                self.__init__()
            elif choice == 'n':
                print("\ncard was not deleted")
                self.__init__()
            else:
                print("\ninvalid input...")
                self._init__()
        else:
            print("\nno card has been inserted...")
            self.__init__()

    def view_card(self, cards):

        i = 1
        if len(cards) > 1:
            for card in cards:
                print(i, ' - ', card[0])
                i += 1
            choice = input("\nwhich card's details do you want to see (b to go back)? ")
            if choice == 'b':
                self.__init__()
            elif not choice.isdigit():
                print("\ninvalid input...")
                self.__init__()
            else:
                choice = int(choice)
                if choice > len(cards):
                    print("\ninvalid input...")
                    self.__init__()
                else:
                    self.cursor.execute(
                        "select * from ΚΑΡΤΑ where αριθμός_κάρτας = '" + str(cards[choice - 1][0]) + "';")
                    info = self.cursor.fetchone()
                    print(
                        "full name: " + str(info[0]) + "\nnumber: " + str(info[1]) + "\nvalid thru: " + str(info[2]) + "\ncvc: " +
                        str(info[3]) + "")
                    self.__init__()

        elif len(cards) == 1:
            self.cursor.execute("select * from ΚΑΡΤΑ where αριθμός_κάρτας = '" + str(cards[0][0]) + "';")
            info = self.cursor.fetchone()
            print(
                "full name: " + str(info[0]) + "\nnumber: " + str(info[1]) + "\nvalid thru: " + str(
                    info[2]) + "\ncvc: " + str(info[3]) + "")
            self.__init__()

    def locs_edit(self, location):

        if location.isalpha():
            location = location.lower()
            location = location.title()
            if location in ['Athina', 'Αθηνα', 'Αθήνα']:
                location = 'Athens'
            if location in ['Patras', 'Πάτρα', 'Πατρα']:
                location = 'Patra'

            return location
        else:
            print("\ninvalid location...")
            self.__init__()

    def check_nearby(self, location):

        self.cursor.execute("select * from ΣΤΑΘΜΟΣ where τόπος = '" + str(location) + "';")
        result = self.cursor.fetchone()

        if result:
            return True
        return False

    def view_stations(self, location=None):

        i = 1
        if location == None:
            self.cursor.execute("select * from ΣΤΑΘΜΟΣ")
            stations = self.cursor.fetchall()
            for station in stations:
                print(i, "- location: " + station[2] + ", address: " + station[-1] + ", telephone: " + str(station[1]) + "")
                i += 1
        else:
            self.cursor.execute("select * from ΣΤΑΘΜΟΣ where τόπος = '" + str(location) + "';")
            stations = self.cursor.fetchall()
            print("\nstations at " + str(location) + " found: " + str(len(stations)) + "")
            for station in stations:
                print(i, "- address: " + station[-1] + ", telephone: " + str(station[1]) + "")
                i += 1

        return i

    def find_free_chargers(self, station_id):

        self.cursor.execute("select αριθμός_θέσης from ΘΕΣΗ where id_σταθμού = '" + str(station_id) + "' and κατειλημμένη = 0;")
        charger = self.cursor.fetchone()
        if charger:
            charger = charger[0]
            return charger
        else:
            return None

    #def turn_appointment_into_charge(self):

        #self.cursor.execute("select αριθμός_φόρτισης, ημερομηνία_φόρτισης from ΦΟΡΤΙΣΗ")
        #dates = self.cursor.fetchall()
        #for date in dates:
        #    if date[1] == datetime.datetime.today().strftime('%Y-%m-%d'):
        #        print(date[1], datetime.datetime.today().strftime('%Y-%m-%d'), date[0])
        #        self.cursor.execute("select αριθμός_ραντεβού, ώρα_άφιξης from ΡΑΝΤΕΒΟΥ where αριθμός_φόρτισης = '" + str(date[0]) + "';")
        #        apps = self.cursor.fetchall()
        #        for app in apps:
        #            num = app[0]
        #            t = app[1]
        #            t = t.split(":")
        #            print(num, t)
        #            if int(t[0]) <= datetime.datetime.now().hour and int(t[1]) <= datetime.datetime.now().minute:
        #                print("11111111111111111", int(t[0]), int(t[1]), num)
        #                self.conn.execute(
        #                    "update ΘΕΣΗ set κατειλημμένη = '" + str(1) + "' where αριθμός_θέσης = '" + str(
        #                        num) + "';")
        #                self.conn.commit()

    def check_name(self, name):

        name = name.split()
        if len(name) != 2:
            return False
        if name[0].isalpha() and name[1].isalpha():
            return True
        return False

    def check_card_num(self, card_number):

        return (self.get_size(card_number) >= 13 and self.get_size(card_number) <= 16) and (
                    self.prefix_matched(card_number, 4) or self.prefix_matched(card_number, 5)
                    or self.prefix_matched(card_number, 37) or self.prefix_matched(card_number, 6)) and (
                    (self.sum_of_double_even_place(card_number) + self.sum_of_odd_place(card_number)) % 10 == 0)

    def sum_of_double_even_place(self, number):
        sum = 0
        num = str(number) + ""
        i = self.get_size(number) - 2
        while (i >= 0):
            sum += self.get_digit(int(str(num[i]) + "") * 2)
            i -= 2
        return sum

    def get_digit(self, number):
        if (number < 9):
            return number
        return int(number / 10) + number % 10

    def sum_of_odd_place(self, number):
        sum = 0
        num = str(number) + ""
        i = self.get_size(number) - 1
        while i >= 0:
            sum += int(str(num[i]) + "")
            i -= 2
        return sum

    def prefix_matched(self, number, d):
        return self.get_prefix(number, self.get_size(d)) == d

    def get_size(self, d):
        num = str(d) + ""
        return len(num)

    def get_prefix(self, number, k):
        if (self.get_size(number) > k):
            num = str(number) + ""
            return int(num[0:k])
        return number

    def check_card_exp(self, year, month):

        if month.isdigit() and year.isdigit():
            if (len(month) == 2 or len(month) == 1) and (len(year) == 4 or len(year) ==2):
                month = int(month)
                if (month < 1 or month > 12):
                    return False
                else:
                    if len(year) == 2:
                        year = '20' + year
                    year = int(year)
                    date = '-'.join([str(year), str(month)])
                    date = date + '-1'
                    date = datetime.datetime.strptime(date, "%Y-%m-%d")
                    if date > datetime.datetime.now():
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    def check_phone_num(self, tel):

        if len(tel) == 10 and tel.isdigit():
            return True
        return False

    def check_email(self, email):

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, email)):
            return True
        return False

    def check_time(self, time):

        try:
            time = time.replace('.',':')
            time = time.split(':')
        except ValueError:
            print("\ninvalid input for time...")
            self.__init__()
        if len(time) == 2:
            hour = time[0]
            minute = time[1]
            if hour.isdigit() and minute.isdigit():
                if (len(hour) == 2 or len(hour) == 1) and (len(minute) == 2 or len(minute) == 1):
                    hour = int(hour)
                    minute = int(minute)
                    if minute < 0 or minute > 59:
                        return False
                    else:
                        if hour < 8 or hour > 20:
                            return False
                        else:
                            return True
                else: return False

    def check_date(self, date):

        try:
            date = date.replace('/', '-')
            date = date.split('-')
        except ValueError:
            print("\ninvalid input for a date...")
            self.__init__()
        if len(date) == 3:
            year = date[0]
            month = date[1]
            day = date[2]
            if month.isdigit() and year.isdigit() and day.isdigit():
                if (len(month) == 2 or len(month) == 1) and (len(year) == 4 or len(year) == 2) and (len(day) == 2 or len(day) == 1):
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12:
                        return False
                    else:
                        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                            if day < 1 or day > 31:
                                print(6)
                                return False
                        elif month == 4 or month == 6 or month == 9 or month == 11:
                            if day < 1 or day > 30:
                                return False
                        else:
                            if day < 1 or day > 28:
                                return False
                        month = str(month)
                        if len(month) == 1:
                            month = '0'+month
                        if len(year) == 2:
                            year = '20' + year
                        year = int(year)
                        date = '-'.join([str(year), str(month), str(day)])
                        #date = datetime.datetime.strptime(date, "%Y-%m-%d")
                        if date >= datetime.datetime.today().strftime('%Y-%m-%d'):
                            return True
                        else:
                            print("\nappointment can't be in the past...")
                            return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_year(self, year):

        if year.isdigit():
            year = int(year)
            if year < 2000:
                return False
            if year > datetime.date.today().year:
                return False
            return True

    def check_plates(self, plates):

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
                      'ΕΥ', 'ΒΟ', 'ΒΒ', 'ΒΑ', 'ΒΤ', 'ΚΜ', 'ΜΖ', 'ΑΗ', 'ΗΟ', 'ΕΕ', 'ΜΜ', 'ΚΝ',
                      'ΤΙ', 'ΡΖ', 'ΤΧ', 'ΡΕ', 'ΡΗ', 'ΚΟ', 'ΚΚ', 'ΤΤ', 'ΜΟ', 'ΜΒ', 'ΕΡ', 'ΙΧ',
                      'ΤΚ', 'ΤΝ', 'ΜΙ', 'ΗΥ', 'ΡΑ', 'ΑΜ', 'ΧΚ', 'ΜΑ', 'ΧΝ', 'ΧΒ', 'ΤΥ', 'ΧΙ',
                      'ΧΟ']
        last_let = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο',
                    'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω']
        plates = plates.split()
        if len(plates) != 2:
            return False
        else:
            if (plates[0].isalpha()) and (plates[1].isdigit()):
                plates[0] = plates[0].upper()
                if (len(plates[0]) == 3) and (len(plates[1]) == 4):
                    if (plates[0][:2] in first_lets) and (plates[0][2] in last_let):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def exit(self):
        self.conn.close()
        exit()

d1 = Edit()
