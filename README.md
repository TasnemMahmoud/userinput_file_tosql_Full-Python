# User Data Management Script

## Overview
This Python script manages user data, allowing users to input, validate, store, and retrieve data. It includes features such as encryption for sensitive data, decryption, file operations, and database interactions. The program uses cryptography for secure data storage and retrieval, and pyodbc for database connectivity.

## Features
- **Data Collection and Validation:** Prompts users for details and validates input for correctness.
- **Data Encryption/Decryption:** Secure user data with AES encryption using the cryptography library.
- **File Management:** Check, create, and manage files for storing encrypted and decrypted data.
- **Database Interaction:** Connect to a SQL Server database, save user data, and retrieve records.
- **User Data Operations:** Collect user data, validate inputs, and manage records.

## Requirements
 -- Python 3.x
 --cryptography library
 --pyodbc library
 -- ODBC Driver 17 for SQL Server (or compatible)

## Instructions
1. **Setup:**
   - Install the `cryptography` library if you haven't already:
     ```bash
     pip install cryptography
     pip install pyodbc

   
2. **Database Configuration:**     
    - Ensure SQL Server is running and accessible.
    - Update the connection parameters in the connect_to_database function to match your SQL Server setup.    


3. **Usage**
   - Generate or Load Encryption Key:
       The script will automatically generate a new encryption key if one doesn't exist. It will save this key to a file named secret.key.

   - File Management:
      The script manages two files:
         user_data.txt: Stores encrypted user data.
         decrypted_data.txt: Stores decrypted user data for viewing.


4. **Run the Script:**
   - Use the following command to run the script:
        python script_name.py

   - Choose from the following options:
         1: Collect new data and save it.
         2: Display all stored data.
         3: Search for a user by ID.
         4: Save decrypted data to a file.
         5: Retrieve all data from the database.
         6: Search for a user by ID from the database.
         7: Exit the program.

5. **Functions**
     - generate_key(): Generates a new encryption key.
     - load_key(): Loads the existing encryption key from a file.
     - save_key(key): Saves the encryption key to a file.
     - encrypt_message(message, key): Encrypts a message using the provided key.
     - decrypt_message(encrypted_message, key): Decrypts an encrypted message using the provided key.
     - check_and_create_file(filename): Checks for the existence of a file and creates it if necessary.
     - load_existing_data(filename): Loads and decrypts existing user data from a file.
     - save_user_data(user_data, filename): Encrypts and saves user data to a file.
     - connect_to_database(): Connects to the SQL Server database.
     - collect_and_save_user_data(user_data): Collects user data, validates it, and saves it to the database.
     - save_decrypted_data_to_file(user_data, output_file): Saves decrypted user data to a file.
     - search_and_save_user_by_id(user_data, output_file): Searches for a user by ID and saves the result to a file.
     - display_all_data(user_data): Displays all user data.
     - search_user_by_id(user_data): Searches for a user by ID and displays the result.
     - retrieve_all_data(): Retrieves and displays all user records from the database.
     - search_user_by_id_from_db(): Searches for a user by ID in the database and displays the result.

6. **Notes**
     - Ensure you have the correct ODBC driver for SQL Server installed.
     - Adjust database connection parameters as needed.
     - The script includes basic error handling for JSON decoding and database operations.

