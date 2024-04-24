import re
import mysql.connector

from Function.System.get_system_info import get_system_info_ext, get_connected_wifi_network
from Function.Conn_BDD.bdd_conn import connect_to_database, close_connection
from Function.SRC.Account_System.verif_new_user import send_verif_mail

def validate_user_data(lastname, firstname, pseudo, email, phonenumber, password, confirm_password):
    confirminfo = 0

    if len(pseudo) < 4:
        print("Le pseudo doit comporter au moins 4 caractères.")
    else:
        confirminfo += 1

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        print("L'adresse email n'est pas valide.")
    else:
        confirminfo += 1

    if not re.match(r'^\+?[0-9]+$', phonenumber):
        print("Le numéro de téléphone n'est pas valide.")
    else:
        confirminfo += 1

    if len(password) < 8 or not any(char.isdigit() for char in password) \
            or not any(char.isupper() for char in password) \
            or not any(char.islower() for char in password) \
            or not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in password):
        print("Le mot de passe doit comporter au moins 8 caractères avec des chiffres, des majuscules, des minuscules et des caractères spéciaux.")
    else:
        confirminfo += 1

    if password != confirm_password:
        print("La confirmation du mot de passe ne correspond pas au mot de passe saisi.")
    else:
        confirminfo += 1

    all_is_correct = confirminfo == 5

    return all_is_correct

def register_user_ext(lastname, firstname, pseudo, email, phonenumber, password, confirm_password):
    if validate_user_data(lastname, firstname, pseudo, email, phonenumber, password, confirm_password):
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO user_account (`lastname`, `firstname`, `pseudo`, `email`, `phone_number`, `password`, `computers_data`, `network`) VALUES ("{lastname}", "{firstname}", "{pseudo}", "{email}", "{phonenumber}", "{password}", "{get_system_info_ext()}", "{get_connected_wifi_network()}")')
                conn.commit()
                cursor.close()
            finally:
                close_connection(conn)
        send_verif_mail(pseudo, email)
        return True
    else:
        return False