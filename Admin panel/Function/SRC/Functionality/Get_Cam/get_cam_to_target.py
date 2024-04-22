import cv2
import socket
import pickle
import struct
from PIL import Image, ImageTk
import threading
import time

class DisplayClient:
    def __init__(self):
        self.keep_running = True
        self.current_socket = None
        self.cap = None

    def release_resources(self):
        if self.cap:
            self.cap.release()
        if self.current_socket:
            self.current_socket.close()

    def receive_and_show(self, label, host_ip):
        # Port d'écoute
        port = 9999
        
        try:
            # Libérer les ressources existantes
            self.release_resources()

            # Création du socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connexion au serveur local du PC cible
            s.connect((host_ip, port))
            self.current_socket = s

            # Boucle principale
            data = b""
            payload_size = struct.calcsize("L")
            while self.keep_running:
                while len(data) < payload_size:
                    data += s.recv(4096)
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += s.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                
                # Chargement du cadre
                frame = pickle.loads(frame_data)
                # Convertir le cadre OpenCV en format d'image Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = frame.resize((635, 450))
                frame = ImageTk.PhotoImage(image=frame)
                # Mettre à jour l'image affichée
                label.img = frame
                label.configure(image=frame)
        except Exception as e:
            print("Erreur :", e)
        finally:
            self.release_resources()

    def start_display(self, label_name, host_ip):
        threading.Thread(target=self.receive_and_show, args=(label_name, host_ip)).start()

    def stop_display(self):
        self.keep_running = False
        time.sleep(0.1)
        self.release_resources()