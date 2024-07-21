import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from .database_unity import DatabaseUnity
import regex as re
from .predict_to_join import PredictToJoin
from .data_visualizating import TeamStatsVisualizating


class JoinToBasketBallGUI:
    def __init__(self, path_of_player_db):
        self.player_db_path = path_of_player_db
        self.window = tk.Tk()
        self.window.geometry("1024x768")
        self.window.title("Bányász Tamás")
        self.window.resizable(False, False)
        
        self.db_unit = DatabaseUnity()
        self.db_unit.create_table(self.player_db_path)
        self.db_unit.create_score_table(self.player_db_path)
        self.predict = PredictToJoin(self.db_unit, self.player_db_path)
        
        self.member_var = StringVar()
        self.center_var = StringVar()
        self.member_var.set("")
        self.center_var.set("")
        
        self.predict_member_label = Label(self.window, textvariable=self.member_var, fg='black', font=('Arial', 15))
        self.predict_member_label.place(x = 150, y = 300)
        
        self.predict_being_center_label = Label(self.window, textvariable= self.center_var, fg='black', font=('Arial', 15))
        self.predict_being_center_label.place(x = 150, y = 350)
        
        self.player_name = None
        self.player_datas = None
        
        self.join_basketball_label = Label(self.window, text='Join to BasketBall Team', fg='black', font=('Arial', 20))
        self.join_basketball_label.pack()
        
        self.entry_name = self.entry_name()
        
        self.height_label = Label(self.window, text='Height (cm)', fg='black', font=('Arial', 15))
        self.height_label.place(x = 450, y = 140)
        
        self.combobox_of_height = self.combobox([i for i in range(150, 201)], 450, 170)
        
        self.sex_label = Label(self.window, text='Gender', fg='black', font=('Arial', 15))
        self.sex_label.place(x = 450, y = 200)
        
        self.combobox_of_gender = self.combobox([i for i in ["Male", "Female"]], 450, 225)
    
        self.send_all_datas_from_player_button()
      
        self.window.mainloop()
    
    def entry_name(self):
        
        name_entry = Entry(self.window)
        name_entry.place(x = 190, y = 173)
        
        name_label = Label(self.window, text='Name :', fg='Black', font=('Ariel', 16))
        name_label.place(x = 117, y = 166)
        
        return name_entry
    
    def get_name(self):
        
        input_name = self.entry_name.get()
        self.entry_name.delete(0, END)
        return input_name

    def combobox(self, value, x_scale, y_scale):
        string_var_for_combobox = tk.StringVar() 
        combobox= ttk.Combobox(self.window, width = 27,  
                            textvariable = string_var_for_combobox) 
        
        combobox['values'] = value
        combobox['state'] = 'readonly'
        
        combobox.place(x = x_scale, y = y_scale)
  
        combobox.current(0)
        
        return combobox
    
    def get_value_from_combobox(self, combobox_value):
        return combobox_value.get()
    
    def check_input_is_correct(self):
        self.player_datas=None
        self.member_var.set("")
        self.center_var.set("")
        
        inputs_correct = True
        
        name = self.get_name()
        height = self.get_value_from_combobox(self.combobox_of_height)
        gender = self.get_value_from_combobox(self.combobox_of_gender)
        
        pattern = r"^[\p{Lu}][\p{L}'-]*$"
        if not re.match(pattern, name, re.UNICODE):
            messagebox.showerror("Error", "Wrong name format")
            inputs_correct = False
            
        elif height == '' or gender == '':
            messagebox.showerror("Error", "Empty property field")
            inputs_correct = False

        self.player_name = name
        return inputs_correct
            
    def player_categorizate(self):
        
        player_is_member = 0
        player_being_center_player = 0
        
        if 195 > int(self.get_value_from_combobox(self.combobox_of_height)) > 180:
            player_is_member = 1
            player_being_center_player = 0
            
        if 180 < int(self.get_value_from_combobox(self.combobox_of_height)) > 195:
            player_is_member = 1
            player_being_center_player = 1
            
        elif int(self.get_value_from_combobox(self.combobox_of_height)) <= 180:
            player_is_member = 0
            player_being_center_player = 0
        
        return player_is_member, player_being_center_player
    
    def get_all_datas_from_player(self):
       
        if self.check_input_is_correct() == True: 
            
            player_is_member, player_being_center_player = self.player_categorizate()            
           
            self.player_datas = [self.player_name, 
                                    int(self.get_value_from_combobox(self.combobox_of_height)),
                                    self.get_value_from_combobox(self.combobox_of_gender),
                                    player_is_member,
                                    player_being_center_player]
        
            print(self.player_datas)
            
            self.db_unit.insert_to_table(self.player_db_path, self.player_datas)
            
            self.db_unit.select_all_data_from_player_properties_table(self.player_db_path)
            
            messagebox.showinfo("Info", "Datas sent.")
            
            last_id_of_player_properties = self.db_unit.get_last_id()
            print("Last id of the player properties table: ", last_id_of_player_properties)
            
            self.db_unit.insert_to_score_table(self.player_db_path, last_id_of_player_properties)
        
        self.combobox_of_height.current(0)
        self.combobox_of_gender.current(0)
        
        self.predict_applicant_what_could_be()
        
        if self.db_unit.get_last_id() >= 15:
            TeamStatsVisualizating(self.player_db_path)
        
        
    def send_all_datas_from_player_button(self):
        send_player_name_button = tk.Button(self.window, text='Send player',
                                       command=lambda: self.get_all_datas_from_player(),
                                       font=('Arial', 16))

        send_player_name_button.place(x = 190, y = 203)
    
    def predict_applicant_what_could_be(self):
        
        if self.db_unit.get_last_id() < 15:
            print("Preparing from mock datas...")
            X, y_member, y_center =self.predict.preparing_the_datas_from_mock_datas_to_predict()
            self.predict.fit_the_modell(X, y_member, y_center)
            
        if self.db_unit.get_last_id() >= 15:
            print("Preparing from db file ...")
            X, y_member, y_center = self.predict.preparing_the_datas_from_db_to_predict()
            self.predict.fit_the_modell(X, y_member, y_center)
        
        try:
            is_member_prediction, is_center_prediction = self.predict.predict_to_being_member_and_center_player(self.player_datas[1], self.player_datas[2])
            print(f'{self.player_datas[0]}--> Prediction to being member: {"Could be member" if is_member_prediction == 1 else "Could not be member"}')
            print(f'{self.player_datas[0]}--> Prediction to be a center player: {"Yes" if is_center_prediction == 1 else "No"}')
        
            self.member_var.set(f'{self.player_datas[0]}--> Prediction to being member: {"Could be member" if is_member_prediction == 1 else "Could not be member"}')
            self.center_var.set(f'{self.player_datas[0]}--> Prediction to be a center player: {"Yes" if is_center_prediction == 1 else "No"}')
            
        except TypeError:
            print("No datas to predict")
        
if __name__ == '__main__':
    JoinToBasketBallGUI()
    
    