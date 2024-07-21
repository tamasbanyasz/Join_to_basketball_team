import http.server
import urllib.parse
from Join_to_a_basketball_team_1_2v import database_unity
import os

"""
    It's a simpe HTTP request. Datas loaded from the 'player.db' file and appears on the HTML page inside tables. 
    We can add to each player score points just we have to fill the inputs field with the players row and the number of score.
    If the score is under 0 then we cannot see the player in the right table.
    
    And here we have to make effeciently how the handle the database file path...
    
    
"""

class WebServer(http.server.SimpleHTTPRequestHandler):
    
    connect_to_db_is = False
    
    if os.path.exists("./Join_to_a_basketball_team_1_2v/player.db"):
        print("Database file is exist.")
        connect_to_db_is = True
    else:
        print("Database file doesn't exist.")
        
    def do_GET(self):
        checked_url= urllib.parse.urlparse(self.path)
        if checked_url.path == '/home':
            self.update_player_datas()
            
    def do_POST(self):
        checked_url= urllib.parse.urlparse(self.path)
        if checked_url.path == '/player_updated':
            self.add_score(self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8'))
            self.redirect()
    
    def add_score(self, data):
        parameters = urllib.parse.parse_qs(data)
        print(parameters)
        try:
            if 'player_row' and 'player_score' in parameters and self.connect_to_db_is:
                player_row = parameters['player_row'][0]
            
                player_score = parameters['player_score'][0]

                print(player_row)
                print(player_score)
            
                database_unity.DatabaseUnity().update_score_table("./Join_to_a_basketball_team_1_2v/player.db", player_row, player_score)
            else:
                print("No connection to db file... Probably missing parameters or no connection.")
        except KeyError:
            print("Wrong 'player_row' input format.")
            
    def update_player_datas(self):
        self.send_response(200)
        self.send_header('Content_type', 'text/html; charset=UTF-8')
        self.end_headers()
    
        self.wfile.write(bytes("<html><meta http-equiv='Content-Type' content='text/html;charset=UTF-8'>"
                               "<body style='background-color:lavender;'>"
                               "<h2>BasketBall Team:</h2>"
                               "<form id = 'user_input' form action='http://localhost:8080/player_updated' method = 'post'>"
                                    "Player Row: <input type = 'text' id='player_rw' name = 'player_row'><br>"
                                    "Player score: <input type = 'text' id = 'player_scr' name = 'player_score'><br>"
                                    "<input type='submit' value= 'Send' /><br><br>"
                                    
                                
                               
                                "</form><br>"
                               
                                "<style> table , th , td {border:1px solid black; margin-left: 30px; text-align: center;  background-color: #ffffff;}</style>"
                                "<body>"
                                "<table style='width:50%'; align='left';>"
                               
                                "<tr > " 
                                "<th width='30px;'> </th>"
                                "<th> Player name </th>"
                                "<th> Player height </th>"
                                "<th width='50px;'> Center Player </th></tr>"
                                , 'UTF-8'))
                               
        
        if self.connect_to_db_is:
            players_data = database_unity.DatabaseUnity().select_all_data_from_player_properties_table("./Join_to_a_basketball_team_1_2v/player.db")
            
            try:
                for index, row in enumerate(players_data, 1):
            
                    self.wfile.write(bytes("<tr>"
                                "<td>"+ str(index) + "</td>"
                                "<td>" + str(row[1]) + "</td>"
                                "<td>" + str(int(row[2])) + " cm" + "</td>"
                                "<td>" + str(int(row[5])) + "</td></tr>", 'UTF-8'))
            except TypeError:
                print("No data from player properties table ...")
            
        self.wfile.write(bytes('</table></body>', 'UTF-8'))
        
        self.wfile.write(bytes("<style> table , th , td {border:1px solid black; margin-right: 40px; text-align: center;  background-color: #ffffff;}</style>"
                                "<body>"
                                "<table style='width:20%'; align='center';>"
                               
                                "<tr > " 
                                "<th width='20px;'> </th>"
                                "<th> Scored player </th>"
                                "<th width='20%;'> Player Score </th></tr>"
                                , 'UTF-8'))
        
        if self.connect_to_db_is:
            players_score = database_unity.DatabaseUnity().select_data_from_score_and_name_where_score_not_null("./Join_to_a_basketball_team_1_2v/player.db")
            
            try:
                for index, row in enumerate(players_score, 1):
                    print(row)
                    self.wfile.write(bytes("<tr>"
                                "<td>"+ str(row[0]) + "</td>"
                                "<td>" + str(row[2]) + "</td>"
                                "<td>" + str(int(row[1])) + "</td></tr>", 'UTF-8'))
            except TypeError:
                print("No datas from score table ...")

        self.wfile.write(bytes('</table></body></html>', 'UTF-8'))
        
        
    def redirect(self):
        self.send_response(303)  
        self.send_header('Location', '/home')
        self.end_headers()

    
http.server.HTTPServer(('localhost', 8080), WebServer).serve_forever()

