import socket
import ipaddress
from scapy.all import ARP, Ether, srp

def get_all_ips_in_network(gateway_ip):
    # Créer un objet réseau à partir de l'adresse de la passerelle
    network = ipaddress.IPv4Network(f"{gateway_ip}/24", strict=False)

    # Récupérer toutes les adresses IP dans le réseau
    all_ips = [str(ip) for ip in network.hosts()]

    return all_ips

def get_connected_devices(ip_range):
    # Créer une requête ARP pour découvrir les adresses IP du réseau
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range)
    
    # Envoyer la requête ARP et recevoir la réponse
    result = srp(arp_request, timeout=3, verbose=0)[0]

    # Extraire les adresses IP et noms des périphériques connectés
    connected_devices = []
    for sent, received in result:
        try:
            # Résolution DNS inverse pour obtenir le nom de la machine
            host_name, _, _ = socket.gethostbyaddr(received.psrc)
            host_name = host_name.split('.')[0]  # Prendre seulement le nom principal
        except socket.herror:
            # Si la résolution DNS inverse échoue, utiliser l'adresse IP comme nom
            host_name = received.psrc
        connected_devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'name': host_name})

    return connected_devices

# Remplacez '192.168.1.1' par l'adresse de votre passerelle
gateway_ip = '192.168.1.254'
ip_range = f"{gateway_ip}/24"

all_ips_in_network = get_all_ips_in_network(gateway_ip)
connected_devices = get_connected_devices(ip_range)

print("Toutes les adresses IP dans le réseau :")
for ip in all_ips_in_network:
    print(ip)

print("\nAdresses IP connectées et utilisées dans le réseau :")
for device in connected_devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}, Nom: {device['name']}")