import mysql.connector

from Function.Conn_BDD.bdd_conn import connect_to_database, close_connection
from Function.SRC.Account_System.user_data import get_user_data

def update_user_info(lastname_var="", firstname_var="", pseudo_var="", email_var="", phonenumber_var="", password_var=""):
    ip_user = get_user_data()[0]
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            if lastname_var.strip() != "":
                cursor.execute(f'UPDATE user_account SET lastname = "{lastname_var}" WHERE id={ip_user}')
            if firstname_var.strip() != "":
                cursor.execute(f'UPDATE user_account SET firstname = "{firstname_var}" WHERE id={ip_user}')
            if pseudo_var.strip() != "":
                cursor.execute(f'UPDATE user_account SET pseudo = "{pseudo_var}" WHERE id={ip_user}')
            if email_var.strip() != "":
                cursor.execute(f'UPDATE user_account SET email = "{email_var}" WHERE id={ip_user}')
            if phonenumber_var.strip() != "":
                cursor.execute(f'UPDATE user_account SET phone_number = "{phonenumber_var}" WHERE id={ip_user}')
            conn.commit()
            cursor.close()
        finally:
            close_connection(conn)