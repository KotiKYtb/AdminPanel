import socket
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