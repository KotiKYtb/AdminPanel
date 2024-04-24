import csv
from ...Conn_BDD.bdd_conn import connect_to_database, close_connection

# Function to get all user data in a csv file when user is connected
def get_user_data():
    user_data = []
    with open("Data/in_use_account.csv", "r") as in_use:
        in_use_reader = csv.reader(in_use)
        next(in_use_reader, None)  # Skip header if exists
        for row in in_use_reader:
            id_user = row[1]
            conn = connect_to_database()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f'SELECT * FROM user_account WHERE id={id_user}')
                    user_data.extend(cursor.fetchone())
                    conn.commit()
                finally:
                    cursor.close()
                    close_connection(conn)
    return user_data