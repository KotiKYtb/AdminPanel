## Project Cam
## Team members

#### Théo BLANDIN (Project Manager)
#### Louis TORCHET--MAILLARD (Developer)

## Project targeted
Le projet demandé concerne un script qui permet d’intercepter le flux vidéo d’une caméra IP basique.

## Project explaination
Dans le cadre de notre cursus en cybersécurité, nous avons choisi ce projet qui nous permet de comprendre le processus d'attaque d'un hacker. Notre projet vise à réaliser une application "panel admin", composée de plusieurs fonctions, telles que la gestion des utilisateurs, l'analyse du réseau, la capture du flux vidéo de la webcam d'une machine dont le script client est installé. 
D'autres options sont installées comme un DDoS, un keylogger, l'envoi d'un mail de phishing via une liste d'adresses mail.

Les données sont sauvegardées et récupérées sur une base de données SQL, reliée à notre serveur Python. Pour finir, le script client s'exécute au démarrage de la machine.

## Utils used

#### IDE used :
- Visual Studio Code

#### Programmation language :
- Python

#### Library used :
- os
- winreg
- getpass -> getuser
- getuser
- customtkinter
- tkinter
- csv
- re
- PIL -> Image
- mysql.connector
- subprocess
- socket
- platform
- getmac -> get_mac_adress
- pickle
- struct
- threading
- time
- smtplib
- email -> encoders/MIMEText/MIMEMultipart/MIMEBase
- ipadresse

## Features
- Gestion des utilisateurs
- Analyse du réseau
- Capture du flux vidéo de la webcam d'une machine
- DDoS (Distributed Denial of Service)
- Keylogger
- Envoi d'un mail de phishing via une liste d'adresses mail
