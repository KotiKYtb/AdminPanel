import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="46.105.155.130",
            port=3306,
            user="u1133_XDDiX8qxHl",
            password="WQ6A=fKw4Rsvf!poL2FM36fG",
            database="s1133_AdminPanel"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def close_connection(conn):
    if conn:
        conn.close()