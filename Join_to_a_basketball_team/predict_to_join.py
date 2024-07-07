from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from database_unity import DatabaseUnity 


class PredictToJoin:
    def __init__(self):
        self.player_db = DatabaseUnity().select_all_data("./Join_to_a_basketball_team/player.db")
        self.player_db_table_column_names = DatabaseUnity().get_column_names("./Join_to_a_basketball_team/player.db")
        self.players_in_df = DataFrame(self.player_db, columns=self.player_db_table_column_names)
        print(self.players_in_df)
        
        self.clf_member = DecisionTreeClassifier()
        self.clf_center = DecisionTreeClassifier()

    def preparing_the_dataframe_to_predict(self):
        
        
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

