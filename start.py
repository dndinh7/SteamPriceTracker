import sqlite3
import track

def main():
    with sqlite3.connect('games.db') as db:
        cur = db.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS games 
                    (id INTEGER PRIMARY KEY, 
                    date TEXT, title TEXT,
                    orig_price REAL, 
                    sale_price REAL, 
                    url TEXT)''')

        res = cur.execute("SELECT name FROM sqlite_master")
        print("You are connected to database:", res.fetchone()[0])
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
        cur.close()
        print("Connection to database is closed")
        
    return

if __name__ == '__main__':
    main()