from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime
import track

# the database is called steam_sales
# the table is called Games

def login():
    try:
        #create_sales_table_query = """
        #(id INT AUTO_INCREMENT PRIMARY KEY,
        #date datetime NOT NULL,   
        #title VARCHAR(100) NOT NULL,
        #orig_price DECIMAL(4, 2),
        #sale_price DECIMAL(4, 2),
        #url VARCHAR(200) NOT NULL)
        #"""

        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database= "steam_sales"
        ) as db:
            mycursor= db.cursor()
            if db.is_connected():
                mycursor.execute("SELECT DATABASE();")
                database_s= mycursor.fetchone()
                print("You're connected to database:", database_s[0])

            command= [""]
            while (len(command) == 0 or command[0] != "exit"): 
                command= input("What do you want to do (add, update, remove, view, exit)? ").split()
                if len(command) == 0:
                    continue
                elif command[0].lower() == "add":
                    if len(command) != 3:
                        print("To add a game, do \"add <game_name> <game_URL>\"")
                        continue
                    name= command[1]
                    url= command[2]
                    if track.add(name, url, db):
                        print("Added {} to database".format(name))
                    else:
                        print("{} already exists".format(name))
                elif command[0].lower() == "remove":
                    if len(command) != 2:
                        print("To remove a game, do \"remove <game_name>\"")
                        continue
                    name= command[1]
                    if track.remove(name, db):
                        print("Removed {} from database".format(name))
                    else:
                        print("{} does not exist".format(name))
                elif command[0].lower() == "update":
                    if len(command) != 1:
                        print("To check for updates, just do \"update\"")
                        continue
                    if track.update(db):
                        print("Checked and updated game prices")
                    else:
                        print("Unable to update games.")
                    
                elif command[0].lower() == "exit":
                    continue
                elif command[0].lower() == "view":
                    if len(command) != 2:
                        print("To view the games, do \"view <sales/all>\"")
                        continue
                    if command[1] == "sales":
                        track.view(db, 0)
                    elif command[1] == "all":
                        track.view(db, 1)
                else:
                    print("You entered an invalid command.")

            #mycursor.execute("CREATE TABLE Games " + create_sales_table_query)
            mycursor.close()
            db.close()
            print("Connection to database is closed")
            
    except Error as e:
        print(e)
            

    

if __name__ == '__main__':
    login()