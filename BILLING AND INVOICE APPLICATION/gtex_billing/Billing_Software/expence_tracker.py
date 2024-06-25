from tkinter import *
from datetime import date
import time
import mysql.connector as sql

tk=Tk()
tk.geometry("1920x1080")
tk.config(bg="#F5F5F5")
tk.title("Expence Tracker - Gayathri Tex")
tk.configure(bg='white')

mycon=sql.connect(host="localhost",user="root",passwd="Gayathri@2404",database="gtex_db")
cursor=mycon.cursor()

def display_block():
    today = date.today()
    show = ("SELECT amount FROM accounts where date = '{date}'".format(date=today))
    cursor.execute(show)
    today_data=cursor.fetchall()

    today_balance_amount = 0.0
    today_from_account = 0.0
    today_to_account = 0.0
    for i in today_data:
        if(i[0] < 0):
            today_from_account += i[0]
        else:
            today_to_account += i[0]

    today_balance_amount = today_to_account + today_from_account
    if(today_from_account < 0):
        today_from_account *= (-1)
        
    month = date.today().month
    show = ("SELECT amount FROM accounts where month(date) = '{month}'".format(month=month))
    cursor.execute(show)
    month_data=cursor.fetchall()
    
    month_balance_amount = 0.0
    month_from_account = 0.0
    month_to_account = 0.0
    for i in month_data:
        if(i[0] < 0):
            month_from_account += i[0]
        else:
            month_to_account += i[0]

    month_balance_amount = month_to_account + month_from_account
    if(month_from_account < 0):
        month_from_account *= (-1)
        

    show = ("SELECT amount FROM accounts")
    cursor.execute(show)
    total_data=cursor.fetchall()

    total_balance_amount = 0.0
    total_from_account = 0.0
    total_to_account = 0.0
    for i in total_data:
        if(i[0] < 0):
            total_from_account += i[0]
        else:
            total_to_account += i[0]

    total_balance_amount = total_to_account + total_from_account
    if(total_from_account < 0):
        total_from_account *= (-1)

    Label(tk,text="This Day",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1055,y=100)
    Label(tk,text="From Amount : {number:06}".format(number=(today_from_account)),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=150)
    Label(tk,text="To Amount : {number:06}".format(number=today_to_account),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=190)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=230)
    Label(tk,text="Balance Amount : {number:06}".format(number=today_balance_amount),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=250)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=270)

    Label(tk,text="This Month",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1045,y=350)
    Label(tk,text="From Amount : {number:06}".format(number=(month_from_account)),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=400)
    Label(tk,text="To Amount : {number:06}".format(number=(month_to_account)),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=440)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=480)
    Label(tk,text="Balance Amount : {number:06}".format(number=month_balance_amount),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=500)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=520)

    Label(tk,text="Total",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1065,y=600)
    Label(tk,text="From Amount : {number:06}".format(number=(total_from_account)),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=650)
    Label(tk,text="To Amount : {number:06}".format(number=total_to_account),font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=690)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=730)
    Label(tk,text="Balance Amount : {number:06}".format(number=total_balance_amount),font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1000,y=750)
    Label(tk,text="- - - - - - - - - - - - - - - - - - - - - - -",font=("Arial", 12),bg="white",fg="#1A374D").place(x=1000,y=770)

def from_account_save():
    particulars = from_particulars_entry.get()
    amount = float(from_amount_entry.get())*(-1)
    today = date.today()
    insert = ("INSERT INTO accounts VALUES('{particulars}',{amount},'{date}')").format(date=today,particulars=particulars,amount=amount)
    cursor.execute(insert)
    mycon.commit()
    from_particulars_entry.delete(0,END)
    from_amount_entry.delete(0,END)
    display_block()
    
def to_account_save():
    particulars = to_particulars_entry.get()
    amount = float(to_amount_entry.get())
    today = date.today()
    insert = ("INSERT INTO accounts VALUES('{particulars}',{amount},'{date}')").format(date=today,particulars=particulars,amount=amount)
    cursor.execute(insert)
    mycon.commit()
    to_particulars_entry.delete(0,END)
    to_amount_entry.delete(0,END)
    display_block()

Label(tk,text="GAYATHRI TEX - ERODE",font=("Arial", 20, "bold"),bg="white",fg="#1A374D").place(x=650,y=20)

'''------- From Account -------'''

Label(tk, text="- - - - - From Account - - - - -",font=("Arial", 13,"bold"),bg="white",fg="#1A374D").place(x=470,y=100)
from_particulars_lable = Label(tk, text="Particulars",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=405,y=150)
from_particulars_entry = Entry(tk,font=("Arial", 12),bd=3)
from_particulars_entry.place(x=350,y=180)

from_amount_lable = Label(tk, text="Amount",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=655,y=150)
from_amount_entry = Entry(tk,font=("Arial", 12),bd=3)
from_amount_entry.place(x=600,y=180)

from_save_button = Button(tk, text="Save",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",width=50,command=from_account_save)
from_save_button.place(x=370,y=230)

'''------- To Account -------'''

Label(tk, text="- - - - - To Account - - - - -",font=("Arial", 13,"bold"),bg="white",fg="#1A374D").place(x=480,y=350)
to_particulars_lable = Label(tk, text="Particulars",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=550,y=400)
to_particulars_entry = Entry(tk,font=("Arial", 12),bd=3)
to_particulars_entry.place(x=350,y=430)

to_amount_lable = Label(tk, text="Amount",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=655,y=400)
to_amount_entry = Entry(tk,font=("Arial", 12),bd=3)
to_amount_entry.place(x=600,y=430)

to_save_button = Button(tk, text="Save",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",width=50,command=to_account_save)
to_save_button.place(x=370,y=480)

'''------- Generate Report -------'''

Label(tk, text="- - - - - Generate Report - - - - -",font=("Arial", 13,"bold"),bg="white",fg="#1A374D").place(x=460,y=600)
from_date_lable = Label(tk, text="From Date",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=400,y=650)
from_date_entry = Entry(tk,font=("Arial", 12),bd=3)
from_date_entry.place(x=350,y=680)

to_date_lable = Label(tk, text="To Date",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=655,y=630)
to_date_entry = Entry(tk,font=("Arial", 12),bd=3)
to_date_entry.place(x=600,y=680)

generate_button = Button(tk, text="Generate Report",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",width=50)
generate_button.place(x=370,y=730)

display_block()
tk.mainloop()