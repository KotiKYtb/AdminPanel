import mysql.connector
from Function.Conn_BDD.bdd_conn import connect_to_database, close_connection
from Function.System.get_system_info import get_connected_wifi_network 

def get_target_ip():
    target_ip = []
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT ip FROM target_ip WHERE network='{get_connected_wifi_network()}'")
            rows = cursor.fetchall()
            for row in rows:
                target_ip.append(row[0])
        finally:
            cursor.close()
            conn.close()
    return target_ip
