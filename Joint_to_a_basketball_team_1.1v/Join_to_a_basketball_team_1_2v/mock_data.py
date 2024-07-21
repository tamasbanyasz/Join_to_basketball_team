
def mock_datas():
    mock_data = {
                    'player_name': ['Test_1', 'Test_2', 'Test_3', 'Test_4', 'Test_5', 'Test_6', 'Test_7', 'Test_8', 'Test_9', 
                    'Test_10', 'Test_11', 'Test_12'],
                    'player_gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
                    'player_height': [180, 180, 181, 181, 195, 195, 196, 196, 179, 179, 182, 182],
                    'team_member': [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                    'being_center_player': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
            }
    return mock_data

if __name__ == '__main__':
        mock_datas()