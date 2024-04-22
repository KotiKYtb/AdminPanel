import csv
import mysql.connector
from ...System.get_system_info import get_system_info_ext
from ...Conn_BDD.bdd_conn import connect_to_database, close_connection

def login_user(login_pseudo_entry, login_password_entry, auto_login_checkbox):
    pseudo = login_pseudo_entry
    password = login_password_entry
    auto_login = auto_login_checkbox
    correct_data = False

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_account WHERE pseudo = %s AND password = %s", (pseudo, password))
            row = cursor.fetchone()

            if row:
                if row[3] == pseudo and row[6] == password:
                    correct_data = True
                if correct_data:
                    # Write to in_use_account.csv
                    with open("Data/in_use_account.csv", "w", newline='') as in_use:
                        in_use_account = csv.writer(in_use)
                        if in_use.tell() == 0:
                            in_use_account.writerow(["Auto Login", "ID", "Pseudo", "Computer's Data"])  # Header
                        in_use_account.writerow([auto_login, row[0], row[3], row[7]])
                    return True
                else:
                    print("Erreur compte !")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

def verif_auto_login_or_not():
    with open("Data/in_use_account.csv", "r") as in_use:
        in_use_reader = csv.reader(in_use)
        next(in_use_reader, None)  # Skip header if exists
        for row in in_use_reader:
            if row[0] == '1':
                return True
    return False