from Join_to_a_basketball_team_1_2v.gui_of_join_basketball_team import JoinToBasketBallGUI

"""
We can run the GUI with the 'main.py' file. We have to fill the 'Name' field with a real, regular name (John, Helena). The input
had to decline: - if the name starts with lowercase letter
                - it has a backspace in the name
                - it has special character in the name
                
Then we have to add a 'Height' and 'Gender' parameter. Then the code determine the applicant can be a team member and it will be a center player or not.
After we sent the parameters the code will show to us on the GUI the applicant could be a member or a center player by predicting.

A database file (player.db) stores the applicant parameters.

It has two table:   - player_properties 
                    - score

The 'player_copy.db' is just a copy file about the original database file if something is went wrong with it we doesn't have to make
new mock datas.

At the first if we doesn't have the 'player.db' file the code use some mock datas from the 'mock_data.py' file.
After (over 15 records) the code working from the database file.
And the code make a 'plot.jpg' file to show the stats about how many male or female is member.

The input formats of name is difficult. It depends on what kind of forms we want to accept as 'valid input'.


"""

def main():
    path_of_player_db = "./Join_to_a_basketball_team_1_2v/player.db"
    join_to_basketball_team = JoinToBasketBallGUI(path_of_player_db)
    
if __name__ == '__main__':
    main()