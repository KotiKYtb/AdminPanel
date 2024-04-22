import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import re
import string
import mysql.connector

from Function.Conn_BDD.bdd_conn import connect_to_database, close_connection
from Function.SRC.CSV.many_csv_function import insert_data_into_csv, return_list_of_data, clear_csv

def generate_code():
    letters_uppercase = string.ascii_uppercase
    letters_lowercase = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    all_characters = letters_uppercase + letters_lowercase + digits + special_characters
    code = ''.join(random.choices(all_characters, k=16))
    while not (re.search(r'[A-Z]', code) and
               re.search(r'[a-z]', code) and
               re.search(r'\d', code) and
               re.search(r'[!@#$%^&*()_+\-=[\]{}|;:,.<>?]', code)):
        code = ''.join(random.choices(all_characters, k=16))
    return code

def insert_verif_data_into_db(code, mail):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f'INSERT INTO mail_vérification (`verification_code`, `mail_in_vérification`, `date`) VALUES ("{code}", "{mail}", NOW())')
            conn.commit()
            cursor.close()
        finally:
            close_connection(conn)

def send_verif_mail(username, destinataire, verif_code=generate_code()):
    # Paramètres du compte Gmail
    email = 'esaipbachelor@gmail.com'
    password = 'rurg urmn piee zllf'

    nom_expéditeur = "Account Vérification"
    nom_signature = "ESAIP"

    # Destinataire et contenu de l'e-mail
    objet = f"{username} | Vérification de votre compte"

    image_path = "Images/signature_esaip_img.jpg"

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
                <p class="p">Bienvenue parmis nous {username} !</p>
                <p class="p">Pour la sécurité de notre environnement, nous avons mis en place un système de vérification par mail.</p>
                <p class="p">Pour cela, vous devez juste copier le code ci-dessous, et le coller dans l'emplacement prévu sur notre application.</p>
            </section>
            <section class="mail_preset">
                <span id="verif_code">{verif_code}</span>
                <p id="copying">Select to copy</p>
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
    # Chemin d'accès à la pièce jointe
    fichier_joint = 'Images/Admin Panel ID Card.png'

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = f"{nom_expéditeur} <{email}>"
    msg['To'] = destinataire
    msg['Subject'] = objet

    # Ajout du contenu du message
    msg.attach(MIMEText(mail, 'html'))

    # Ajout de la pièce jointe
    with open(fichier_joint, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    with open(image_path, 'rb') as image_file:
        image = MIMEBase('application', 'octet-stream')
        image.set_payload(image_file.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {fichier_joint}')

    msg.attach(part)
    encoders.encode_base64(image)
    image.add_header('Content-ID', '<signature_image>')

    msg.attach(image)

    # Connexion au serveur SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    # Envoi de l'e-mail
    texte = msg.as_string()
    server.sendmail(email, destinataire, texte)

    # Fermeture de la connexion au serveur SMTP
    server.quit()
    insert_verif_data_into_db(verif_code, destinataire)
    file_path = "Function/SRC/CSV/temp_verif_data.csv"
    temp_data_list = [verif_code, destinataire]
    clear_csv(file_path)
    insert_data_into_csv(temp_data_list, file_path)

send_verif_mail("KotiK", "blandintheo.pro@gmail.com")

def verif_code_mail(entry_code_verif):
    file_path = "Function/SRC/CSV/temp_verif_data.csv"
    data_verif_list = return_list_of_data(file_path)
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT verification_code FROM mail_vérification WHERE mail_in_vérification = '{data_verif_list[1]}'")
            # Récupération du code de vérification depuis la base de données
            verif_code = cursor.fetchone()
            while cursor.nextset():
                cursor.fetchall()
            conn.commit()
            cursor.close()
            # Vérification si le code entré correspond au code de la base de données
            if verif_code and entry_code_verif.get() == data_verif_list[0]:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE user_account SET account_verif=1 WHERE email='{data_verif_list[1]}'")
                conn.commit()
                cursor.close()
                return True
            else:
                return False
        finally:
            close_connection(conn)
