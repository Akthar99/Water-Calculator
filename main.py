import os 
import time
from datetime import date 
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Time:
    def __init__(self) -> None:
        pass

    # return the current time 
    def get_time(self):
        current_time = time.ctime()
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
    
    def time_count(self):
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
        self.var_value = 0
    
    # create a label for print time 
    def timer(self):
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
    def add(self):
        self.var += 50
        self.amount.config(text=f"{self.var} ml")
    def sub(self):
        self.var -= 50
        self.amount.config(text=f"{self.var} ml")
    def except_button_anwser(self):
        if (self.var < 0):
            msg = messagebox.showerror("Error on Input", "below zero error.. please enter above zero")
        else:
            self.var_value = self.var
            new_window.destroy()
            print(self.var_value)
            self.button.config(state=NORMAL)
    def cancel_btn(self):
        self.var_value = 0
        new_window.destroy()
        print(self.var_value)
        self.button.config(state=NORMAL)
    def closed(self):
        self.button.config(state=NORMAL)
        new_window.destroy()
    # this method create a exra window to get the user input 
    # after getting user inputs it automatically close the window and store a value that user entered in a variable 
    def handle_button(self):
        self.button.config(state=DISABLED)
        global new_window
        new_window = tk.Toplevel()
        new_window.title("Get the water amount")
        new_window.geometry("400x200")
        new_window.maxsize(400,200)
        ttk.Label(new_window, text="Chose the amount you drinked", font=("Helvetica", 10), foreground="black").pack()
        self.var = 50
        button1 = ttk.Button(new_window, text="+", command=self.add)
        button1.pack()
        self.amount = ttk.Label(new_window, text=f"{self.var} ml", font=("Helvetica", 10), foreground="black")
        self.amount.pack()
        button2 = ttk.Button(new_window, text="-", command=self.sub)
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
        new_window.protocol("WM_DELETE_WINDOW", self.closed)

    # create a button for the user input 
    def Input_button(self):
        print(self.var_value)
        self.button = ttk.Button(self.sec_frame, text="Drink Water", command=self.handle_button, width=30)
        self.button.pack(padx=20, pady=20)

    # run the window and this method include mainloop 
    def run(self):
        self.timer()
        self.update_time()
        self.date_section()
        self.Input_button()
        print(self.time.get_time())
        self.root.mainloop()



if __name__ == "__main__":
    app = App()
    app.run()