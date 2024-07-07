from gui_of_join import JoinToBasketBallGUI

"""
We can run the code with the 'main.py' file. We have to fill the 'Name' field with a real, regular name. Then we have to add
a 'Height' and 'Gender' parameter. Then the code determine the applicant can be a team member and it will be a center player or not.
After we sent the parameters the code will show to us on the GUI the applicant could be a member or a center player byy predicting.

A database file stores the applicant parameters.

The 'player_copy.db' is just a copy file about the original database file if something is went wrong with it we doesn't have to make
new mock datas.

But we run the code without any exist db file we will get error at the prediction part. 

"""

def main():
    join_to_basketball_team = JoinToBasketBallGUI()
    
if __name__ == '__main__':
    main()