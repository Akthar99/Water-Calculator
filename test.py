import sqlite3
# from main import Time as time

# class Datebase:
#     def __init__(self):
#         self.time = time()
#     @staticmethod
#     def runQuery(sql, receive=False):
#         connection = sqlite3.connect("database.db")
#         cursor = connection.cursor()
#         if receive:
#             return cursor.fetchall()
#         else:
#             cursor.execute(sql)
#         connection.commit()

#         connection.close()


#     def get_and_print_wait_time(self):
#         query = f"insert into waterTable values ({self.time.datetime()}, 3, 2, 3)"
#         print(str(self.time.datetime()))
#         self.runQuery(sql=query)
#     def all_in_database(self):
#         query = f"SELECT * FROM waterTable"
#         print(self.runQuery(query, None, True))
    
    

#     def insert_into_database(self):
#         query = f"INSERT INTO waterTable (wait_time) VALUES (3)"
#         self.runQuery(query) 
# database = Datebase()
# # database.get_and_print_wait_time()

import pandas as pd
import matplotlib.pyplot as plt

def matplot():
    data1 = [3,4,2,4,5]
    data2 = [5,6,7,8,9]

    dataframe = pd.DataFrame({"x": data1, "y": data2})

    plt.scatter(dataframe["x"], dataframe["y"])

    data3 = [1,2,3,4,5]
    data4 = [5,6,7,6,5]

    plt.plot(data3, data4, color="green", linestyle="--")

    plt.title("Data analyzer")
    plt.xlabel("x-label")
    plt.ylabel("y-label")

    plt.show()

def panda():
    colunms = ["name", "age", "height", "weight"]
    titleed_colunms = pd.DataFrame({"name": ["John", "Alice", "Hasiru"], "age": [23, 22, 21], "height": [32,44,47], "weight": [23, 45, 47]})
    # selecting column data 
    select_colunm = titleed_colunms["name"]
    print(titleed_colunms["name"][2]) # selecting one item from the column
    # selecting row data
    select_row = titleed_colunms.loc[1]
    print(select_row)

    # manupulate data
    bmi = []
    # weight/height^2
    for i in range(len(titleed_colunms)):
        bmi.append(titleed_colunms["weight"][i]/ titleed_colunms["height"][i]**2)
    
    titleed_colunms["bmi"] = bmi
    print(titleed_colunms)

    # saving to csv file 
    titleed_colunms.to_csv("data.csv", index=False, sep="\t")

    # reading from csv file
    read_data = pd.read_csv("data.csv", sep="\t")
    print(read_data)

    # reading sqlite database 
    connection = sqlite3.connect("database.db")
    sql_data = pd.read_sql("select * from waterDetail", connection)
    print(sql_data)

    # filtering data
    filter_sql_data = sql_data[sql_data["water_amount"] > 200]
    print(filter_sql_data)

    # replacing data
    replace_data = sql_data.replace(200, 0)
    print(replace_data)
    # drop
    # remove_duplicated_data = sql_data.drop_duplicates()
panda()

import tkinter as tk
def on_option_select():
    selected = selected_option.get()
    result_label.config(text=f"Selected Option: {selected}")
root = tk.Tk()
root.title("Dropdown Menu Example")
root.geometry("400x300")
# Create a StringVar to hold the selected option
selected_option = tk.StringVar()
# Create the dropdown menu
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack(pady=10)
# Add a button to display the selected option
show_button = tk.Button(root, text="Show Selection", command=on_option_select)
show_button.pack()
# Label to display the selected option
result_label = tk.Label(root, text="")
result_label.pack()
root.mainloop()