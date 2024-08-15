import os
import json
import pyodbc
from cryptography.fernet import Fernet


filename = 'user_data.txt'
output_file = 'decrypted_data.txt'  


def generate_key():
    return Fernet.generate_key()

def load_key():
    return open("secret.key", "rb").read()

def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

if not os.path.exists("secret.key"):
    key = generate_key()
    save_key(key)
else:
    key = load_key()


def check_and_create_file(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass
        print(f"File {filename} created.")
    else:
        print(f"File {filename} already exists.")


def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            encrypted_data = file.read()
            if encrypted_data:
                try:
                    decrypted_data = decrypt_message(encrypted_data.encode(), key)
                    return json.loads(decrypted_data)
                except json.JSONDecodeError:
                    print("Error decoding JSON data.")
                    return {}
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return {}
    return {}


def save_user_data(user_data, filename):
    with open(filename, 'w') as file:
        encrypted_data = encrypt_message(json.dumps(user_data), key)
        file.write(encrypted_data.decode())


def connect_to_database():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'         
        'DATABASE=UserDatabase;' 
        'UID=Tasnem;'         
        'PWD=tosa123456;'          
    )


def collect_and_save_user_data(user_data):
    conn = connect_to_database()
    cursor = conn.cursor()

    user_id = input("Enter User ID: ")
    if user_id in user_data:
        print("ID already exists. Cannot enter data.")
        conn.close()
        return

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    age = input("Enter age: ")
    gender = input("Enter gender (Male/Female/Other): ")
    year_of_birth = input("Enter year of birth: ")

    
    if not user_id.isalnum():
        print("Invalid User ID. It must be alphanumeric.")
        conn.close()
        return
    if not first_name.isalpha() or not last_name.isalpha():
        print("First or last name is invalid. It must contain letters only.")
        conn.close()
        return
    if not age.isdigit() or int(age) <= 0:
        print("Invalid age. It must be a positive integer.")
        conn.close()
        return
    if gender not in ['Male', 'Female', 'Other']:
        print("Invalid gender. Choose from the provided options.")
        conn.close()
        return
    if not year_of_birth.isdigit() or len(year_of_birth) != 4 or int(year_of_birth) > 2023 - 18:
        print("Invalid year of birth. Ensure the user is not younger than 18 years.")
        conn.close()
        return

    user_data[user_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "age": int(age),
        "gender": gender,
        "year_of_birth": int(year_of_birth)
    }

    insert_query = """
    INSERT INTO Users (user_id, first_name, last_name, age, gender, year_of_birth) VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (
        user_id,
        first_name,
        last_name,
        int(age),
        gender,
        int(year_of_birth)
    ))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data saved successfully to the database.")


def save_decrypted_data_to_file(user_data, output_file):
    with open(output_file, 'w') as file:
        for user_id, details in user_data.items():
            file.write(f"ID: {user_id}\n")
            file.write(f"  First Name: {details['first_name']}\n")
            file.write(f"  Last Name: {details['last_name']}\n")
            file.write(f"  Age: {details['age']}\n")
            file.write(f"  Gender: {details['gender']}\n")
            file.write(f"  Year of Birth: {details['year_of_birth']}\n")
            file.write("\n")


def search_and_save_user_by_id(user_data, output_file):
    user_id = input("Enter User ID to search: ")
    if user_id in user_data:
        details = user_data[user_id]
        with open(output_file, 'w') as file:
            file.write(f"ID: {user_id}\n")
            file.write(f"  First Name: {details['first_name']}\n")
            file.write(f"  Last Name: {details['last_name']}\n")
            file.write(f"  Age: {details['age']}\n")
            file.write(f"  Gender: {details['gender']}\n")
            file.write(f"  Year of Birth: {details['year_of_birth']}\n")
    else:
        print("ID not found.")


def display_all_data(user_data):
    for user_id, details in user_data.items():
        print(f"ID: {user_id}")
        print(f"  First Name: {details['first_name']}")
        print(f"  Last Name: {details['last_name']}")
        print(f"  Age: {details['age']}")
        print(f"  Gender: {details['gender']}")
        print(f"  Year of Birth: {details['year_of_birth']}\n")


def search_user_by_id(user_data):
    user_id = input("Enter User ID to search: ")
    if user_id in user_data:
        details = user_data[user_id]
        print(f"ID: {user_id}")
        print(f"  First Name: {details['first_name']}")
        print(f"  Last Name: {details['last_name']}")
        print(f"  Age: {details['age']}")
        print(f"  Gender: {details['gender']}")
        print(f"  Year of Birth: {details['year_of_birth']}\n")
    else:
        print("ID not found.")


def retrieve_all_data():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM Users"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        print("\nAll User Records:")
        for row in rows:
            print(f"ID: {row.user_id}")
            print(f"  First Name: {row.first_name}")
            print(f"  Last Name: {row.last_name}")
            print(f"  Age: {row.age}")
            print(f"  Gender: {row.gender}")
            print(f"  Year of Birth: {row.year_of_birth}")
            print()
    else:
        print("No records found.")

    cursor.close()
    conn.close()


def search_user_by_id_from_db():
    user_id = input("Enter User ID to search: ")
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM Users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()

    if row:
        print(f"\nUser Record for ID {user_id}:")
        print(f"  First Name: {row.first_name}")
        print(f"  Last Name: {row.last_name}")
        print(f"  Age: {row.age}")
        print(f"  Gender: {row.gender}")
        print(f"  Year of Birth: {row.year_of_birth}")
    else:
        print("ID not found.")

    cursor.close()
    conn.close()


def main():
    check_and_create_file(filename)
    user_data = load_existing_data(filename)
    
    while True:
        print("\nChoose an option:")
        print("1. Collect new data")
        print("2. Display all stored data")
        print("3. Search for a user by ID")
        print("4. Save decrypted data to file")
        print("5. Retrieve all data from database")
        print("6. Search for a user by ID from database")
        print("7. Exit the program")

        choice = input("Enter your choice: ")

        if choice == '1':
            collect_and_save_user_data(user_data)
            save_user_data(user_data, filename)
            print("Data saved successfully.")
        elif choice == '2':
            display_all_data(load_existing_data(filename))
        elif choice == '3':
            search_user_by_id(load_existing_data(filename))
        elif choice == '4':
            user_data = load_existing_data(filename)
            save_decrypted_data_to_file(user_data, output_file)
            print(f"Decrypted data saved to file {output_file}.")
        elif choice == '5':
            retrieve_all_data()
        elif choice == '6':
            search_user_by_id_from_db()
        elif choice == '7':
            save_user_data(user_data, filename)
            print("All data saved. Exiting the program.")
            break
        else:
            print("Invalid option. Please enter a valid number.")

if __name__ == "__main__":
    main()
