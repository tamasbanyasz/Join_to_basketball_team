from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from .mock_data import mock_datas


class PredictToJoin:
    def __init__(self, database_of_players, player_db_path):
        self.mocks = mock_datas()
        self.player_db = database_of_players
        self.all_datas_from_player_properties = self.player_db.select_all_data_from_player_properties_table(player_db_path)
        self.player_db_properties_table_column_names = self.player_db.get_column_names(player_db_path)
        self.players_in_df = DataFrame(self.all_datas_from_player_properties, columns=self.player_db_properties_table_column_names)
        print(self.players_in_df)
        
        self.clf_member = DecisionTreeClassifier()
        self.clf_center = DecisionTreeClassifier()
    
    def preparing_the_datas_from_mock_datas_to_predict(self):
        mock_datas = DataFrame(self.mocks)
        mock_datas['player_gender'] = mock_datas['player_gender'].apply(lambda x: 0 if x == 'Male' else 1)

        X = mock_datas[['player_height', 'player_gender']]
        y_member = mock_datas['team_member']
        y_center = mock_datas['being_center_player']
        
        return X, y_member, y_center

    def preparing_the_datas_from_db_to_predict(self):
        
        self.players_in_df['player_gender'] = self.players_in_df['player_gender'].apply(lambda x: 0 if x == 'Male' else 1)

        X = self.players_in_df[['player_height', 'player_gender']]
        y_member = self.players_in_df['team_member']
        y_center = self.players_in_df['being_center_player']
        
        return X, y_member, y_center
        
        
    def fit_the_modell(self, X, y_member, y_center):
        try:
            X_train, X_test, y_train_member, y_test_member = train_test_split(X, y_member, test_size=0.2, random_state=42)
            _, _, y_train_center, y_test_center = train_test_split(X, y_center, test_size=0.2, random_state=42)

            self.clf_member.fit(X_train, y_train_member)
            self.clf_center.fit(X_train, y_train_center)
        except ValueError:
            print("No datas to predict")
            
    def predict_to_being_member_and_center_player(self, height, gender):

        gender_num = 0
        if gender == 'Male':
            gender_num = 0
        else:
            gender_num = 1
    
        new_player_data = DataFrame({'player_height': [height], 'player_gender': [gender_num]})
    
        is_member = self.clf_member.predict(new_player_data)[0]
        is_center = self.clf_center.predict(new_player_data)[0]
    
        return is_member, is_center

if __name__ == '__main__':
    PredictToJoin()

