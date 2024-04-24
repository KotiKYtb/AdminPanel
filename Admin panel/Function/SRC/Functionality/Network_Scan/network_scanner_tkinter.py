import tkinter as tk
from tkinter import ttk
from scapy.all import ARP, Ether, srp
import ipaddress
import socket

def get_all_ips_in_network(gateway_ip):
    network = ipaddress.IPv4Network(f"{gateway_ip}/24", strict=False)
    all_ips = [str(ip) for ip in network.hosts()]
    return all_ips

def get_connected_devices(ip_range):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range)
    result = srp(arp_request, timeout=3, verbose=0)[0]
    connected_devices = []
    for sent, received in result:
        try:
            host_name, _, _ = socket.gethostbyaddr(received.psrc)
            host_name = host_name.split('.')[0]
        except socket.herror:
            host_name = received.psrc
        connected_devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'name': host_name})
    return connected_devices

def create_gui(all_ips, connected_devices):
    root = tk.Tk()
    root.title("Network Scanner")
    root.geometry("600x400")
    root.configure(bg="#001a33")

    title_label = ttk.Label(root, text="Network Scanner", font=("Helvetica", 20), foreground="#33ccff", background="#001a33")
    title_label.pack(pady=20)

    all_ips_label = ttk.Label(root, text="All IPs in the network:", font=("Helvetica", 12), foreground="#33ccff", background="#001a33")
    all_ips_label.pack()

    all_ips_text = tk.Text(root, height=6, width=50, font=("Helvetica", 10), wrap="none", foreground="#33ccff", background="#00264d")
    all_ips_text.insert("1.0", "\n".join(all_ips))
    all_ips_text.pack(pady=10)

    connected_devices_label = ttk.Label(root, text="Connected Devices:", font=("Helvetica", 12), foreground="#33ccff", background="#001a33")
    connected_devices_label.pack()

    connected_devices_text = tk.Text(root, height=10, width=50, font=("Helvetica", 10), wrap="none", foreground="#33ccff", background="#00264d")
    for device in connected_devices:
        connected_devices_text.insert("end", f"IP: {device['ip']}, MAC: {device['mac']}, Name: {device['name']}\n")
    connected_devices_text.pack(pady=10)

    root.mainloop()

# Replace '192.168.1.1' with your gateway address
gateway_ip = '192.168.1.254'
ip_range = f"{gateway_ip}/24"

all_ips_in_network = get_all_ips_in_network(gateway_ip)
connected_devices = get_connected_devices(ip_range)

create_gui(all_ips_in_network, connected_devices)