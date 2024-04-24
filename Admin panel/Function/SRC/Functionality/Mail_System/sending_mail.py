import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_mail(destinataire, template):
    # Paramètres du compte Gmail
    email = 'esaipbachelor@gmail.com'
    password = 'rurg urmn piee zllf'

    match template:
        case "esaip":
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
                <title>☠️ Admin Panel ☠️ | Envoi d'informations</title>
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
                    <h1 id="titre">Envoi d'informations</h1>
                    <section class="mail_preset">
                        <a href="https://drive.google.com/file/d/1tG1BtKdD4RJfP7PmJBqI0pWiINKUY8Sh/view?usp=sharing">Compte Rendu</a>
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
        case "credit agricole":
            nom_expéditeur = "Crédit Agricole"
            nom_signature = "Votre conseiller"

            # Destinataire et contenu de l'e-mail
            objet = "Votre demande d’activation de l'option «Paiement à distance»"
            mail = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>☠️ Admin Panel ☠️ | Envoi d'informations</title>
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
                    <h1 id="titre">Envoi d'informations</h1>
                    <section class="mail_preset">
                        <a href="https://drive.google.com/file/d/1tG1BtKdD4RJfP7PmJBqI0pWiINKUY8Sh/view?usp=sharing">Compte Rendu</a>
                    </section>
                    <section id="signature">
                        <img id="image_sign" src="cid:signature_image" alt="ESAIP Signature">
                        <ul id="un_list">
                            <li class="list_item">
                                <p>Crédit Agricole</p>
                            </li>
                            <li class="list_item">
                                <p>Votre conseiller</p>
                            </li>
                            <li class="list_item">
                                <p>DUPONT Bertrand</p>
                            </li>
                            <li class="list_item">
                                <p>06 60 32 21 08</p>
                            </li>
                            <li class="list_item">
                                <p>Votre Agence</p>
                            </li>
                            <li class="list_item" id="last_li">
                                <p>2 Rte de Beaufort, 49124 Saint-Barthélemy-d'Anjou CEDEX</p>
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
        case "bouygues":
            nom_expéditeur = "Bouygues Telecom"
            nom_signature = "© 2024 Bouygues Telecom"

            # Destinataire et contenu de l'e-mail
            objet = "Votre facture Bouygues Telecom est disponible"
            mail = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>☠️ Admin Panel ☠️ | Envoi d'informations</title>
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
                    <h1 id="titre">Envoi d'informations</h1>
                    <section class="mail_preset">
                        <a href="https://drive.google.com/file/d/1tG1BtKdD4RJfP7PmJBqI0pWiINKUY8Sh/view?usp=sharing">Compte Rendu</a>
                    </section>
                    <section id="signature">
                        <img id="image_sign" src="cid:signature_image" alt="ESAIP Signature">
                        <ul id="un_list">
                            <li class="list_item">
                                <p>Bouygues Telecom</p>
                            </li>
                            <li class="list_item">
                                <p>Votre ligne</p>
                            </li>
                            <li class="list_item">
                                <p>DUPONT Bertrand</p>
                            </li>
                            <li class="list_item">
                                <p>06 60 32 21 08</p>
                            </li>
                            <li class="list_item">
                                <p>Votre Opérateur</p>
                            </li>
                            <li class="list_item" id="last_li">
                                <p>75 Av. Montaigne, 49000 Angers CEDEX</p>
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
        case _:
            pass

    # Charger l'image
    with open("Images/signature_esaip_img.jpg", "rb") as fichier_image:
        image_mime = MIMEBase('image', 'png')
        image_mime.set_payload(fichier_image.read())

    # Encodage de l'image en base64
    encoders.encode_base64(image_mime)

    # Ajout de l'en-tête pour le CID
    image_mime.add_header('Content-ID', '<signature_image>')

    # Ajout de l'image au message
    msg.attach(image_mime)

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = f"{nom_expéditeur} <{email}>"
    msg['To'] = destinataire
    msg['Subject'] = objet

    # Ajout du contenu du message
    msg.attach(MIMEText(mail, 'html'))

    # Connexion au serveur SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    # Envoi de l'e-mail
    texte = msg.as_string()
    server.sendmail(email, destinataire, texte)

    # Fermeture de la connexion au serveur SMTP
    server.quit()