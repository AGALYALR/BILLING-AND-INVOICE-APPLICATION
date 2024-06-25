from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
import time
from tkinter import messagebox
import mysql.connector as sql

tk=Tk()
tk.geometry("1920x1080")
tk.config(bg="#F5F5F5")
tk.title("Delivery Slip - Gayathri Tex")
tk.configure(bg='white')

mycon=sql.connect(host="localhost",user="root",passwd="Gayathri@2404",database="gtex_db")
cursor=mycon.cursor()

show = ("SELECT COUNT(*) FROM delivery_slip")
cursor.execute(show)
slip_no=cursor.fetchall()
slip_no=int(slip_no[0][0])+1

def clear_item():
    particulars_entry.delete(0,END)
    quantity_entry.delete(0,END)
    quantity_entry.insert(0, "0")
    
delivery_list = []
def add_item():
    particulars = particulars_entry.get()
    quantity = int(quantity_entry.get())
    delivery_item = [particulars, quantity]
    tree.insert('',0, values=delivery_item)
    clear_item()
    delivery_list.append(delivery_item)
    
    
def generate_delivery_slip():
    doc = DocxTemplate("delivery_slip_template.docx")
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_number_entry.get()
    gst = gst_entry.get()
    dsno = "DS-2425-{number:06}".format(number=slip_no)
    current_date = datetime.date.today()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    doc.render({"name":name,
                "address":address,
                "phone":phone,
                "gst":gst,
                "deliveryno": dsno,
                "deliverydate":current_date,
                "deliverytime":current_time,
                "delivery_list": delivery_list})
    
    doc_name = "DS-2425-{number:06}".format(number=slip_no)+".docx"
    doc.save('E:/gtex_billing/Billing_Software/Delivery Slips/'+doc_name)    
    particulars_data = ""
    quantity_data = ""
    price_data = ""
    amount_data = ""
    
    for i in range(len(delivery_list)):
        particulars_data += delivery_list[i][0]
        quantity_data += str(delivery_list[i][1])
                
        if(i<len(delivery_list)-1):
            particulars_data += ","
            quantity_data += ","
                
    insert = ("INSERT INTO delivery_slip VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')").format(dsno,current_date,current_time,name,address,phone,gst,particulars_data,quantity_data)
    cursor.execute(insert)
    mycon.commit()
    messagebox.showinfo("Invoice Complete", "Invoice Complete")
    
def clear_delivery_slip():
    name_entry.delete(0,END)
    address_entry.delete(0,END)
    phone_number_entry.delete(0,END)
    gst_entry.delete(0,END)
    
    particulars_entry.delete(0,END)
    quantity_entry.delete(0,END)
    quantity_entry.insert(0, "0")
        
    for item in tree.get_children():
        tree.delete(item)

a = Label(tk,text="AJRA TEX - KARUR",font=("Arial", 20, "bold"),bg="white",fg="#1A374D").place(x=650,y=20)
slip_number_label = Label(tk,text="Delivery Slip Number : DS-2425-{number:06}".format(number=slip_no),font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1200,y=20)

'''------- Buyer details -------'''

name_label = Label(tk, text="Name",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=260,y=100)
name_entry = Entry(tk,font=("Arial", 12),bd=3)
name_entry.place(x=190,y=130)

address_label = Label(tk, text="Address",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=560,y=100)
address_entry = Entry(tk,font=("Arial", 12),bd=3)
address_entry.place(x=500,y=130)

phone_number_label = Label(tk, text="Phone number",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=850,y=100)
phone_number_entry = Entry(tk,font=("Arial", 12),bd=3)
phone_number_entry.place(x=810,y=130)

gst_label = Label(tk, text="GST number",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=1160,y=100)
gst_entry = Entry(tk,font=("Arial", 12),bd=3)
gst_entry.place(x=1110,y=130)

'''------- Product details -------'''

particulars_label = Label(tk, text="Particulars",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=550,y=180)
particulars_entry = Entry(tk,font=("Arial", 12),bd=3)
particulars_entry.place(x=500,y=210)

quantity_label = Label(tk, text="Quantity",font=("Arial", 12,"bold"),bg="white",fg="#1A374D").place(x=870,y=180)
quantity_entry = Spinbox(tk, from_=1,to=100,font=("Arial", 12),bd=3)
quantity_entry.place(x=810,y=210)

add_item_button = Button(tk, text="Add item",font=("Arial", 10,"bold"),bg="#1A374D",fg="#F5F5F5",command=add_item)
add_item_button.place(x=1110,y=210)

columns = ('particulars', 'quantity')
tree = ttk.Treeview(tk, columns=columns, show="headings")
tree.heading('particulars', text='Particulars')
tree.heading('quantity', text='Quantity')
tree.place(x=580,y=300)

save_slip_button = Button(tk, text="Generate Delivery Slip",font=("Arial",10,"bold"),bg="#1A374D",fg="#F5F5F5",width=30,height=2,command=generate_delivery_slip)
save_slip_button.place(x=650,y=580)
new_slip_button = Button(tk, text="Clear Delivery Slip",font=("Arial",10,"bold"),bg="#1A374D",fg="#F5F5F5",width=30,height=2,command=clear_delivery_slip)
new_slip_button.place(x=650,y=640)
edit_slip_button = Button(tk, text="Edit Delivery Slip",font=("Arial",10,"bold"),bg="#1A374D",fg="#F5F5F5",width=30,height=2)
edit_slip_button.place(x=650,y=700)

tk.mainloop()
