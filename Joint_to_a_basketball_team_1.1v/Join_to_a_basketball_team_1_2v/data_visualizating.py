import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator
from .database_unity import DatabaseUnity
import numpy as np


class TeamStatsVisualizating:
    def __init__(self, path_of_the_player_db):
        self.players_data = DatabaseUnity().select_all_data_from_player_properties_table(path_of_the_player_db)
        self.player_data_in_df = pd.DataFrame(self.players_data, columns=DatabaseUnity().get_column_names(path_of_the_player_db))
        

        self.player_data_in_df['player_gender'] = self.player_data_in_df['player_gender'].replace({1: 'Male', 0: 'Female'})
        self.player_data_in_df['team_member'] = self.player_data_in_df['team_member'].replace({1: 'Yes', 0: 'No'})
        
        self.membership_counts = self.player_data_in_df.groupby(['player_gender', 'team_member']).size().unstack(fill_value=0)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))


        self.r1 = np.arange(len(self.membership_counts))
        self.r2 = [x + 0.35 for x in self.r1]


        self.ax.bar(self.r1, self.membership_counts['Yes'], color='green', width= 0.35, edgecolor='grey', label='Is member')
        self.ax.bar(self.r2, self.membership_counts['No'], color='orange', width= 0.35, edgecolor='grey', label='Is not member')


        self.ax.set_xlabel('Gender', fontweight='bold')
        self.ax.set_ylabel('Number of players', fontweight='bold', )
        self.ax.set_title('Membership counting by gender')
        self.ax.set_xticks([r + 0.35 / 2 for r in range(len(self.membership_counts))])
        self.ax.set_xticklabels(self.membership_counts.index)


        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))


        self.ax.legend()


        plt.tight_layout()
        plt.savefig('plot.jpg')
        plt.close()
        
        
if __name__ == '__main__':
    TeamStatsVisualizating()

