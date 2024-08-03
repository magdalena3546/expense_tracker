import sqlite3

# function for set connection with sqlite
def create_connection(file_db):
    try:
        con = sqlite3.connect(file_db)
        # print(f"Connected with database: {file_db}")
        return con
    
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    
# function to create tables
def create_tables(con):
    try: 
        cursor = con.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                    )
                '''
            )

        cursor.execute ('''
            CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TEXT NOT NULL
                    )
        '''
            )

        cursor.execute ('''
            CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                    )
        '''
            )
        print("Tables were created.")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def insert_categories(con, categories):
    cursor = con.cursor()
    for category in categories:
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", category)
        except sqlite3.IntegrityError:
            print(f"Category '{category[0]}' already exists")
    con.commit()