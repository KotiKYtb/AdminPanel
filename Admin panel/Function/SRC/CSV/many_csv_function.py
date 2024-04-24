import csv

# Function to know if a file is empty or not, return True if empty
def csv_is_empty_or_full(file_path):
    with open(file_path, 'r', newline='') as file:
        return not any(row for row in file)
    
# Function to clear a csv file
def clear_csv(file_path):
    with open(file_path, 'w', newline='') as file:
        file.write('')

# Function to return True if in a csv file the Auto Login column == 0 (user not activate Auto Login)
def search_auto_login_in_csv(file_path):
    with open(file_path, 'r', newline='') as file:
        file_reader = csv.reader(file)
        if file.tell() > 0:
            next(file_reader, None)
        else:
            pass
        for row in file:
            if row[0] == "0":
                return True
            else:
                return False

def return_list_of_data(file_path):
    data_list = []
    try:
        # Ouvre le fichier CSV en mode lecture
        with open(file_path, 'r', newline='') as file:
            # Crée un objet lecteur CSV
            csv_reader = csv.reader(file)
            # Lit chaque ligne du fichier CSV
            for row in csv_reader:
                # Ajoute la ligne (liste) à la liste des données
                data_list.extend(row)
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
    return data_list

def insert_data_into_csv(list_of_data, file_path):
    try:
        # Ouvre le fichier CSV en mode écriture, en créant un nouveau fichier s'il n'existe pas
        with open(file_path, 'w', newline='') as file:
            # Crée un objet écrivain CSV
            csv_writer = csv.writer(file)
            # Écrit chaque ligne de données dans le fichier CSV
            for data in list_of_data:
                # Join the elements of the list into a string before writing it to the CSV file
                csv_writer.writerow([''.join(data)])
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")