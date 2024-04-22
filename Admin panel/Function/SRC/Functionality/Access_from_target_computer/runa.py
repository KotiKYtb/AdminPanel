import os
import subprocess

def run_as_admin():
    script_path = os.path.abspath("Downloads/runa.bat")
    subprocess.Popen(["runas", "/noprofile", "/user:Administrator", script_path], shell=True)

# Utilisation de la fonction run_as_admin pour exécuter le script batch
run_as_admin()