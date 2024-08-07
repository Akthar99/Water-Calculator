import os 
import time
import datetime as dt
from datetime import date, datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import pickle

class Time:
    def __init__(self) -> None:
        pass

    # return the current time 
    def get_time(self):
        current_time = int(time.time())
        return current_time
    
    # this method return a tuple of ("hour", "minute", "second")
    def clock(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")

        return f"{hour} : {minute} : {second}"
    
    # method return a tuple of ("year", "month", "day")
    def datetime(self):
        today = date.today()

        year = today.strftime("%Y")
        month = today.strftime("%B")
        day = today.strftime("%d")
        
        return year, month, day
    
    # this method creates a timer countdown 
    def timer(self):
        pass

class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.maxsize(400,400)
        self.root.title("Water Calculator")
        self.time = Time()
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(column=0, row=0)
        self.sec_frame = ttk.Frame(self.root, padding=10)
        self.sec_frame.grid(column=0, row=1)
        self.database = Datebase()

        # Logic variables 
        self.var_value = 0
        self.water_list = []
        self.second_window_open = False
        self.send_notification = True
        # Load the variable from the pickle file
        with open('src/my_data.pkl', 'rb') as file:
            settings = pickle.load(file)
        self.wait_time = settings["wait_time"]
        self.wait_time_count = settings["wait_time_count"]


    # create the database and tables 
    # create two tabeles waterTable and waterDetail
    @staticmethod
    def create_database():
        database = Datebase()
        timer = Time()
        waterTable = "CREATE TABLE waterTable (date date primary key, wait_time integer default 0, water integer)"
        waterDetail = "CREATE TABLE waterDetail (date date references waterTable(date), time integer, water_amount integer, foreign key(date) references waterTable(date))"
        today = datetime.now().strftime("%Y-%m-%d")
        query2_data = [str(today), timer.get_time(), 0, 0]
        database.runQuery(waterTable)
        database.runQuery(waterDetail)
        database.runQuery(f'INSERT INTO waterTable VALUES ("{query2_data[0]}", {query2_data[2]}, {query2_data[3]})')
    
    # check if this is a new day or not 
    def check_new_day(self):
        today = datetime.now().strftime("%Y-%m-%d")
        query = f"SELECT date FROM waterTable WHERE date = '{today}'"
        result = self.database.runQuery(query, None, True)
        if not result:
            query2_data = [str(today), self.time.get_time(), 0, 0]
            self.database.runQuery(f'INSERT INTO waterTable VALUES ("{query2_data[0]}", {query2_data[2]}, {query2_data[3]})')
    
    # check if the program is closed before the timer is finished
    def check_remaining_time(self):
        today = datetime.now().strftime("%Y-%m-%d")
        query = f"SELECT wait_time FROM waterTable WHERE date = '{today}'"
        result = self.database.runQuery(query, None, True)
        if result[0][0]:
            self.wait_time = result[0][0]
    
    # create a label for print time 
    def show_time(self):
        self.time_label = ttk.Label(self.frame, text="", font=("Helvetica", 20), foreground="green")
        self.time_label.pack(padx=20, pady=20)

    # update the timer label every second passed by calling get_time method on Time class
    # config - update the arguments in Label. in our case updating the text field of the label
    # after - loop over a function to update the contexts
    def update_time(self):
        self.current_time = self.time.clock()
        self.time_label.config(text=self.current_time)
        self.time_label.after(1000, self.update_time)

    # create a label to peint date 
    def date_section(self):
        current_date = self.time.datetime()
        self.date_label = ttk.Label(self.frame, text=current_date, font=("Helvetica", 20), foreground="green")
        self.date_label.pack(pady=20, padx=20)


    # below three methods is used for the except_button_anwser() method
    def add(self, label, amount):
        self.var += amount
        self.amount.config(text=f"{self.var} {label}")
    def sub(self, label, amount):
        self.var -= amount
        self.amount.config(text=f"{self.var} {label}")
    def except_button_anwser(self):
        if (self.var <= 0):
            msg = messagebox.showerror("Error on Input", "below zero or zero error.. please enter above zero")
        else:
            self.var_value = self.var
            new_window.destroy()
            self.water_list.append(self.var_value)
            print(self.water_list)
            
            # add the water amount and details to the database 
            self.database.runQuery(f"INSERT INTO waterDetail VALUES ('{datetime.now().strftime('%Y-%m-%d')}', {self.time.get_time()}, {self.var_value})")

            self.button.config(state=DISABLED)
            self.second_window_open = False
            # Give the timer how much time to wait in seconds 
            self.wait_time += self.wait_time_count
            
    def cancel_btn(self):
        self.var_value = 0
        new_window.destroy()
        self.second_window_open = False
        print(self.var_value)
        self.button.config(state=NORMAL)
    def closed(self):
        self.button.config(state=NORMAL)
        self.second_window_open = False
        new_window.destroy()

    # this method create a exra window to get the user input 
    # after getting user inputs it automatically close the window and store a value that user entered in a variable 
    def handle_button(self):
        global new_window
        new_window = tk.Toplevel()
        new_window.title("Get the water amount")
        new_window.geometry("400x200")
        new_window.maxsize(400,200)
        ttk.Label(new_window, text="Chose the amount you drinked", font=("Helvetica", 10), foreground="black").pack()
        self.var = 50
        button1 = ttk.Button(new_window, text="+", command=lambda : self.add(amount=50, label="ml"))
        button1.pack()
        self.amount = ttk.Label(new_window, text=f"{self.var} ml", font=("Helvetica", 10), foreground="black")
        self.amount.pack()
        button2 = ttk.Button(new_window, text="-", command=lambda : self.sub(amount=50, label="ml"))
        button2.pack()
        except_button = ttk.Button(new_window, text="OK", command=self.except_button_anwser)
        except_button.pack(padx=10,
                           pady=20,
                           side='right',
                           expand=True)
        cancel_button = ttk.Button(new_window, text="Cancel", command=self.cancel_btn)
        cancel_button.pack(padx=10,
                           pady=20,
                           side='left',
                           expand=True)
        self.second_window_open = True
        self.button.config(state=DISABLED)
        new_window.protocol("WM_DELETE_WINDOW", self.closed)

    # create a button for the user input 
    def Input_button(self):
        # print(self.var_value)
        self.button = ttk.Button(self.sec_frame, text="Drink Water", command=self.handle_button, width=30)
        self.button.pack(padx=20, pady=20)

    # return the 3 hour countdown time
    def timer_countdown(self):

        pass
    
    # update the timer using logics and config method 
    # handle waitin time, button state and notify the user when the timer is finished
    def update_timer(self):
        if self.wait_time == 0 and self.second_window_open == False:
            self.button.config(state=NORMAL)
            # since we send the notification every 5 minutes we need to check the time
            notification_wait_time = int(time.strftime("%M"))
            # if the time is 2 minutes then send the notification once a time
            if notification_wait_time % 2 == 0 and int(time.strftime("%S")) == 0:
                GiveNotification("Time is up!", "Time is up ! drink water 💧").send_notification() # send the notification  
        elif self.wait_time != 0:
            self.button.config(state=DISABLED)
        self.timer_count = dt.timedelta(seconds= self.wait_time)
        if self.wait_time != 0:
            self.wait_time -= 1
        self.timer_label.config(text=f"{self.timer_count}")
        self.timer_label.after(1000, self.update_timer)


    # create a timer label
    def timer(self):
        self.timer_time = self.timer_countdown()
        self.timer_label = ttk.Label(self.sec_frame, text="0:0:0",  font=("Helvetica", 20), foreground="green")
        self.timer_label.pack(padx=10,
                              pady=20,
                              expand=True)
        
    # creating a menu to show the analysis of the data 
    def show_data(self):
        self.dataAnalizer = DataAnalize()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.data_menu = Menu(self.menu, tearoff=0)
        # data vitualiZing menu
        self.menu.add_cascade(label="Data", menu=self.data_menu)
        self.data_menu.add_command(label="Today", command=self.dataAnalizer.today_graph)
        self.data_menu.add_command(label="Week", command=self.dataAnalizer.week_graph)
        self.data_menu.add_command(label="Time Analyze", command=self.dataAnalizer.time_analyze)
        # creating settings menu 
        self.settings_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        # add a check button to turn on and off the notification default is on
        self.settings_menu.add_checkbutton(label="Notification", command=self.notification, onvalue=True, offvalue=False)
        # add a command to change the wait time of the timer
        self.settings_menu.add_command(label="Change Wait Timer", command=self.change_wait_time)
    
    # create a notification method to turn on and off the notification
    def notification(self):
        if self.send_notification:
            self.send_notification = False
        else:
            self.send_notification = True
    # change the wait time of the timer
    def change_wait_time(self):
        # create a new window to get the user input
        self.change_wait_time_wnd = tk.Toplevel()
        self.change_wait_time_wnd.title("Change Timer")
        self.change_wait_time_wnd.geometry("400x200")
        self.change_wait_time_wnd.maxsize(400,200)
        ttk.Label(self.change_wait_time_wnd, text="Chose the time interval you perfer", font=("Helvetica", 10), foreground="black").pack()
        self.var2 = 60
        button1 = ttk.Button(self.change_wait_time_wnd, text="+", command=lambda: self.add(amount=60, label="sec"))
        button1.pack()
        self.amount = ttk.Label(self.change_wait_time_wnd, text=f"{self.var} sec", font=("Helvetica", 10), foreground="black")
        self.amount.pack()
        button2 = ttk.Button(self.change_wait_time_wnd, text="-", command=lambda: self.sub(amount=60, label="sec"))
        button2.pack()
        except_button = ttk.Button(self.change_wait_time_wnd, text="OK", command=self.change_wait_time_anwser)
        except_button.pack(padx=10,
                           pady=20,
                           side='right',
                           expand=True)
        cancel_button = ttk.Button(self.change_wait_time_wnd, text="Cancel", command=lambda: self.change_wait_time_wnd.destroy())
        cancel_button.pack(padx=10,
                            pady=20,
                            side='left',
                            expand=True)
        self.second_window_open = True
        self.button.config(state=DISABLED)
        self.change_wait_time_wnd.protocol("WM_DELETE_WINDOW", self.cwtwn_closed)
    def change_wait_time_anwser(self):
        if (self.var <= 0):
            msg = messagebox.showerror("Error on Input", "below zero or zero error.. please enter above zero")
        else:
            self.wait_time_count = self.var
            self.change_wait_time_wnd.destroy()
            self.second_window_open = False
            self.button.config(state=NORMAL)
            print(self.wait_time)
    # close chaange wait time window 
    def cwtwn_closed(self):
        self.button.config(state=NORMAL)
        self.second_window_open = False
        self.change_wait_time_wnd.destroy()

    # save the data to database before quit the program
    # save the remaining time and water amount to the database
    def close_window(self):
        query = f"UPDATE waterTable SET wait_time = {self.wait_time} WHERE date = '{datetime.now().strftime('%Y-%m-%d')}'"
        self.database.runQuery(query)
        # update the water amount of the day
        # first get the water from table 
        water = self.database.runQuery(f"SELECT water FROM waterTable WHERE date = '{datetime.now().strftime('%Y-%m-%d')}'", receive=True)[0][0]
        # add the calculated water amount
        self.database.runQuery(f"UPDATE waterTable SET water = {water + sum(self.water_list)} WHERE date = '{datetime.now().strftime("%Y-%m-%d")}'")
        # print the remaining time if the user closed the program while running the timer
        self.get_and_print_wait_time()
        self.root.destroy()

    def get_and_print_wait_time(self):
        query = f"SELECT * FROM waterTable"
        self.remain_wait_time = self.database.runQuery(sql=query, receive=True)
        print(self.remain_wait_time)

    # run the window and this method include mainloop 
    def run(self):
        self.check_new_day()
        self.check_remaining_time()
        self.show_data()
        self.show_time()
        self.update_time()
        self.date_section()
        self.Input_button()
        self.timer()
        self.update_timer()
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

class Datebase:
    def __init__(self):
        pass
    def runQuery(self, sql, data:list=None, receive=False):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        if receive:
            result = cursor.execute(sql)
            return result.fetchall()
        else:
            cursor.execute(sql)
        connection.commit()

        connection.close()

# creating new class to analize and visualize the data
# using matplotlib and pandas
import pandas as pd
import matplotlib.pyplot as plt
class DataAnalize:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.waterTable = pd.read_sql("SELECT * FROM waterTable", self.connection)
        self.waterDetail = pd.read_sql("SELECT * FROM waterDetail", self.connection)
        self.connection.close()
    
    # today water collection graph
    def today_graph(self):
        today = datetime.now().strftime("%Y-%m-%d")
        data = self.waterTable[self.waterTable["date"] == today]
        print(data)
        plt.bar(data["date"], data["water"])
        # plt.plot(data["time"], data["water_amount"])
        plt.title("Today Water Collection")
        plt.xlabel("Date")
        plt.ylabel("Water Amount")
        plt.show()

    # week water collection graph
    def week_graph(self):
        data = self.waterTable
        plt.bar(data["date"], data["water"])
        plt.title("Week Water Collection")
        plt.xlabel("Date")
        plt.ylabel("Water Amount")
        plt.show()

    # time analyze graph
    def time_analyze(self):
        day = datetime.now().strftime("%Y-%m-%d")
        data = self.waterDetail[self.waterDetail["date"] == day]

        # manipulate date to get the time in HH:MM:SS format
        data["time"] = pd.to_datetime(data["time"], unit="s").dt.strftime("%H:%M:%S")

        plt.bar(data["time"], data["water_amount"])
        # plt.scatter(data["time"], data["water_amount"])
        plt.title("Time Analyze")
        plt.xlabel("Time")
        plt.ylabel("Water Amount")
        plt.show()

# import the winnotify module to send the notification
from winotify import Notification, audio
# create a class to send a notification 
# <a href="https://www.flaticon.com/free-icons/water" title="water icons">Water icons created by Freepik - Flaticon</a>
class GiveNotification:
    def __init__(self, title:str, message:str):
        self.title = title
        self.message = message
        self.app_id = "Water Calculator"
        self.icon = r"C:\GODOT\Python\Git Clone\Water-Calculator\src\water-bottle.png"
        # send the notification
        self.send_notification()

    def send_notification(self):
        toast = Notification(app_id=self.app_id,
                     title=self.title,
                     msg=self.message,
                     icon=self.icon)

        toast.show()

        
if __name__ == "__main__":
    app = App()
    if not os.path.isfile("database.db"):
        app.create_database()
    app.run()