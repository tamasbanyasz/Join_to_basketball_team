import sqlite3
from sqlite3 import Error


class DatabaseUnity:
    def __init__(self):
        self.last_id_of_player_properties = 0

    def create_table(self, db_name):
        with sqlite3.connect(db_name) as connection:
            
            create_player_table = """
                CREATE TABLE IF NOT EXISTS player_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    player_height INTEGER NOT NULL,
                    player_gender TEXT NOT NULL,
                    team_member INTEGER,
                    being_center_player INTEGER
                    
                );
            """ 
            try:
                cursor = connection.cursor()
                cursor.execute(create_player_table)
                connection.commit()
    
            except Error as e:
                print(e)
    
    def create_score_table(self, db_name):
        with sqlite3.connect(db_name) as connection:
            
            create_score_table = """CREATE TABLE IF NOT EXISTS score (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_id INTEGER UNIQUE,
                            player_score INTEGER,
                            FOREIGN KEY(player_id) REFERENCES player_properties(id)

                        );
                    """
            try:
                cursor = connection.cursor()
                cursor.execute(create_score_table)
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
            self.last_id_of_player_properties = cursor.lastrowid
            
    def insert_to_score_table(self, db_name, id):
        with sqlite3.connect(db_name) as connection:
            insert_into_score_table = """INSERT INTO score(player_id, player_score) VALUES(?, 0);"""
            
            cursor = connection.cursor()
            cursor.execute(insert_into_score_table, (id,))
            connection.commit()
            
    def get_last_id(self):
        return self.last_id_of_player_properties
            
    def get_column_names(self, db_name):
        with sqlite3.connect(db_name) as connection:
            
            get_table_column_names = """PRAGMA table_info(player_properties)"""
            cursor = connection.cursor()
            cursor.execute(get_table_column_names)
            
            return [row[1] for row in cursor.fetchall()]
    
    def update_score_table(self, db_name, player_row, value):
        with sqlite3.connect(db_name) as connection:
            
            check_player_id_exists = f"""
            SELECT CASE 
                WHEN EXISTS(SELECT score.player_id 
                FROM score
                WHERE score.player_id = {player_row}) 
                    THEN 1
                    ELSE 0 
            END;"""

            try:
                
                cursor = connection.cursor()
                cursor.execute(check_player_id_exists)
                connection.commit()

                rows = cursor.fetchone()
                print(f"Player founded: " + str({rows[0]}) + " (bool value)")

                if rows[0] == 1:
                    print("Player is exist to modify 'score' data.")
                
                    update_player_score = f"""UPDATE score SET player_score={value} WHERE score.player_id={player_row};"""

                    cursor.execute(update_player_score)
                    connection.commit()

                if rows[0] == 0:
                    print("Player has not found to modify 'score' data.")
                    
            except Error as e:
                print("Wrong input format to store data ...", e)
    
    
    def select_all_data_from_player_properties_table(self, db_name):
        with sqlite3.connect(db_name) as connection:
    
            select_all_player_data = """SELECT * FROM player_properties"""
            
            datas_from_db_file = None
            
            try:
                cursor = connection.cursor()
                cursor.execute(select_all_player_data)
                
                db_row = cursor.fetchone()
                while db_row is not None:
                    yield db_row
                        
                    db_row = cursor.fetchone()
                
            except Error as e:
                print("Table doesn't exist yet...", e)
                
            return datas_from_db_file
    
    def select_data_from_score_and_name_where_score_not_null(self, db_name):
        with sqlite3.connect(db_name) as connection:
            query_from_score_table= """SELECT score.player_id, score.player_score, player_properties.player_name 
                                        FROM score, player_properties 
                                        WHERE (score.player_id = player_properties.id AND score.player_score > 0);"""
            
            datas_returned_from_score_table = None
            try:
                cursor = connection.cursor()
                cursor.execute(query_from_score_table)
    
                db_row = cursor.fetchone()
                while db_row is not None:
                    yield db_row
                        
                    db_row = cursor.fetchone()
                    
            except Error as e:
                print("Table doesn't exist yet...", e)
                
            return datas_returned_from_score_table
    
            
if __name__ == "__main__":
    DatabaseUnity()
    
    