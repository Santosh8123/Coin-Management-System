import mysql.connector
from tabulate import tabulate

# Function to display Message 
def logo():
    data_str = ""  
    print(data_str.center(80, '-'))
    name = "| WELCOME TO THE COIN MANAGEMENT SYSTEM |"
    print(name.center(80, '*'))
    print(data_str.center(80, '-'))
    print(" ")


# Function to establish connection with the MySQL database
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass1234",
        database="information_of_coins"
    )
    
    return connection



# Function to create a table for the coin collection in the database
def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS coins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        country VARCHAR(255),
        denomination VARCHAR(50),
        year_of_minting INT,
        current_value FLOAT,
        acquired_date DATE
    )
    """
    cursor.execute(query)
    connection.commit()
    connection.close()

# Function to add a new coin to the collection
def add_coin():
    connection = connect_to_database()
    cursor = connection.cursor()

    country = input("\nEnter the country: ")
    denomination = input("Enter the denomination: ")
    year_of_minting = int(input("Enter the year of minting: "))
    current_value = float(input("Enter the current value: "))
    acquired_date = input("Enter the acquired date (YYYY-MM-DD): ")
    if len(acquired_date)==10:
        query = "INSERT INTO coins (country, denomination, year_of_minting, current_value, acquired_date) VALUES (%s, %s, %s, %s, %s)"
        values = (country, denomination, year_of_minting, current_value, acquired_date)

        cursor.execute(query, values)
        connection.commit()
        print("\nNew coin added successfully:\n")

        headers = ["Coin_id", "Country", "Denomination", "Year of minting", "Current value", "Acquired date"]
        new_coin_data = [[cursor.lastrowid, country, denomination, year_of_minting, acquired_date, current_value]]
        print(tabulate(new_coin_data, headers=headers, tablefmt="grid", floatfmt=".2f"))
    else:
        print("Enter a date in the given format.")

    print("-"*100)
    connection.close()
# Function to search for coins based on different criteria
def search_coin():
    connection = connect_to_database()
    cursor = connection.cursor()
    print("\nSearch by:")
    print("\t1. Coin ID")
    print("\t2. Country")
    print("\t3. Year of Minting")
    print("\t4. Current Value (sorted)")
    print("\t5. search by combination")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        coin_id = input("\nEnter the Coin ID: ")
        query = "SELECT * FROM coins WHERE id = %s"
        values = (coin_id,)
    elif choice == 2:
        country = input("\nEnter the country: ")
        query = "SELECT * FROM coins WHERE country = %s"
        values = (country,)

    elif choice == 3:
        year_of_minting = int(input("\nEnter the year of minting: "))
        query = "SELECT * FROM coins WHERE year_of_minting = %s"
        values = (year_of_minting,)

    elif choice == 4:
        query = "SELECT * FROM coins ORDER BY current_value"
        values = None
    elif choice == 5:
        print("\t1. Country + Denomination")
        print("\t2. Country + Year of Minting")
        print("\t3. Country + Denomination + Year of Minting")
       
        choice1 = int(input("Enter your choice: "))
        if choice1 == 1:
            country = input("\nEnter the country: ")
            denomination = input("Enter the denomination: ")
            query = "SELECT * FROM coins WHERE country = %s AND denomination = %s"
            values = (country, denomination)

        elif choice1 == 2:
            country = input("\nEnter the country: ")
            year_of_minting = int(input("Enter the year of minting: "))
            query = "SELECT * FROM coins WHERE country = %s AND year_of_minting = %s"
            values = (country, year_of_minting)

        elif choice1 == 3:
            country = input("\nEnter the country: ")
            denomination = input("Enter the denomination: ")
            year_of_minting = int(input("Enter the year of minting: "))
            query = "SELECT * FROM coins WHERE country = %s AND denomination = %s AND year_of_minting = %s"
            values = (country, denomination, year_of_minting)
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice.")
        return

    cursor.execute(query, values)
    results = cursor.fetchall()

    if not results:
        print("\nNo coins found.")
    else:
        print("\nCoins Found:\n")
        table_data = [list(coin) for coin in results]
        headers = ["Coin_id", "Country", "Denomination", "Year of minting", "Current value", "Acquired date"]
        print(tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".2f"))
    print("-"*100)
    connection.close()

# Funtion to display updated with required information
def update_coin():
    connection = connect_to_database()
    cursor = connection.cursor()

    coin_id = int(input("\nEnter the ID of the coin to update: "))

    query = "SELECT * FROM coins WHERE id = %s"
    values = (coin_id,)
    cursor.execute(query, values)
    coin = cursor.fetchone()

    if not coin:
        print("\nCoin not found.")
    else:
        print("\nCurrent details of the coin:")
        headers = ["Coin_id", "Country", "Denomination", "Year of minting", "Current value", "Acquired date"]
        print(tabulate([coin], headers=headers, tablefmt="grid", floatfmt=".2f"))

        country = input("Enter the new country: ")
        denomination = input("Enter the new denomination: ")
        year_of_minting = int(input("Enter the new year of minting: "))
        current_value = float(input("Enter the new current value: "))
        acquired_date = input("Enter the new acquired date (YYYY-MM-DD): ")

        query = "UPDATE coins SET country = %s, denomination = %s, year_of_minting = %s, current_value = %s, acquired_date = %s WHERE id = %s"
        values = (country, denomination, year_of_minting, current_value, acquired_date, coin_id)

        cursor.execute(query, values)
        connection.commit()
        print("\nCoin updated successfully.")
        print("\nUpdated details of the coin:")
        updated_coin = [coin_id, country, denomination, year_of_minting, current_value, acquired_date]
        print(tabulate([updated_coin], headers=headers, tablefmt="grid", floatfmt=".2f"))

    print("-"*100)
    connection.close()

def delete_coin():
    connection = connect_to_database()
    cursor = connection.cursor()

    coin_id = int(input("\nEnter the ID of the coin to delete: "))

    query = "SELECT * FROM coins WHERE id = %s"
    values = (coin_id,)
    cursor.execute(query, values)
    coin = cursor.fetchone()

    if not coin:
        print("\nCoin not found.")
    else:
        print("\nDetails of the coin to be deleted:")
        headers = ["Coin_id", "Country", "Denomination", "Year of minting", "Current value", "Acquired date"]
        print(tabulate([coin], headers=headers, tablefmt="grid", floatfmt=".2f"))
        confirm = input("Are you sure you want to delete this coin? (y/n): ").lower()
        if confirm == "y":
            query = "DELETE FROM coins WHERE id = %s"
            values = (coin_id,)
            cursor.execute(query, values)
            connection.commit()
            print("\nCoin deleted successfully.")
            print("\nUpdated table after deletion:")
            print_final_table()
        else:
            print("\nDeletion canceled.")
    print("-"*100)
    connection.close()
    
# Function to store the current state of the collection in the database
def store_data():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM coins"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    print("-"*100)
    return results

# Function to print the final updated table of the database
def print_final_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    sql='select * from coins'
    cursor.execute(sql)
    records = cursor.fetchall()
    headers = ["Coin_id", "Country", "Denomination", "Year of Minting","Current Value", "Acquired Date" ]
    table_data = [list(record) for record in records]
    print(tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".2f"))
    print("-"*100)

# Main function to run the application
def main():
    create_table()
    while True:
        logo()
        print("\tMenu:\n\t1. Add coin\n\t2. Update coin\n\t3. Delete coin\n\t4. Search/Display coin\n \
        \b5. Store data in the database\n\t6. Display All Coin Details \n\t7. EXIT")
        
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_coin()
        elif choice == 2:
            update_coin()
        elif choice == 3:
            delete_coin()
        elif choice == 4:
            search_coin()
        elif choice == 5:
            data = store_data() 
            print("Data stored.")
        elif choice == 6:
            data=store_data()
            if data:
                print_final_table()
            else:
                print("No data stored yet.")
        elif choice == 7:
            print('Thanku You....!')
            print("*"*100)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()