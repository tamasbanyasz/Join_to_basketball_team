import sqlite3
from sqlite3 import Error


class DatabaseUnity:
    def __init__(self):
        print("SQLite version: ", sqlite3.version)

    def create_table(self, db_name):
        with sqlite3.connect(db_name) as connection:
            
            create_player_table = """
                CREATE TABLE IF NOT EXISTS player_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    player_height INTEGER NOT NULL,
                    player_gender TEXT NOT NULL,
                    team_member INTEGER NOT NULL,
                    being_center_player INTEGER NOT NULL
                    
                );
            """ 
    
            try:
                cursor = connection. cursor()
                cursor.execute(create_player_table)
                connection.commit()
    
            except Error as e:
                print(e) 
                
    def insert_to_table(self, db_name, value):
        with sqlite3.connect(db_name) as connection:
        
            insert_into_players_table = """INSERT INTO player_properties(player_name, 
                player_height, player_gender, team_member, being_center_player)
                VALUES (?, ?, ?, ?, ?);
    
            """
            cursor = connection.cursor()
            cursor.execute(insert_into_players_table, value)
            connection.commit()
    
    def get_column_names(self, db_name):
        with sqlite3.connect(db_name) as connection:
            
            get_table_column_names = """PRAGMA table_info(player_properties)"""
            cursor = connection.cursor()
            cursor.execute(get_table_column_names)
            
            return [row[1] for row in cursor.fetchall()]
    
    
    def select_all_data(self, db_name):
        with sqlite3.connect(db_name) as connection:
        
            select_all_player_data = """SELECT * FROM player_properties"""
    
            cursor = connection.cursor()
            cursor.execute(select_all_player_data)
    
            datas_from_db_file = cursor.fetchall()
    
            for row in datas_from_db_file:
                print(row)
            
            return datas_from_db_file


if __name__ == "__main__":
    DatabaseUnity()
    
    