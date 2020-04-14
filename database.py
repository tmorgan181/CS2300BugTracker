from tkinter import *
import sqlite3

root = Tk()
root.title("Bug Tracker")
root.geometry("400x400")

#Connect to database
conn = sqlite3.connect("bugTracker.db")

#Create database cursor
c = conn.cursor()

#Create Ticket table if not already present
try:
    c.execute("""CREATE TABLE Tickets (
        ticket_id integer,
        title text,
        description text,
        date_created integer,
        status text,
        priority text,
        ticket_type text
        )""")
except(sqlite3.OperationalError):
    print("Table \'Tickets\' already exists")

#Commit changes
conn.commit()

#Close connection
conn.close()

#Submit function
def submit():
    #Connect to database
    conn = sqlite3.connect("bugTracker.db")

    #Create database cursor
    c = conn.cursor()

    #Insert into table
    c.execute("""INSERT INTO Tickets VALUES (:ticket_id, :title, :description,
        :date_created, :status, :priority, :ticket_type)""",
        {
            "ticket_id": ticket_id.get(),
            "title": title.get(),
            "description": description.get(),
            "date_created": date_created.get(),
            "status": status.get(),
            "priority": priority.get(),
            "ticket_type": ticket_type.get()
        })

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

    #Clear text boxes
    ticket_id.delete(0, END)
    title.delete(0, END)
    description.delete(0, END)
    date_created.delete(0, END)
    status.delete(0, END)
    priority.delete(0, END)
    ticket_type.delete(0, END)

    return

#Query function
def query():
    #Connect to database
    conn = sqlite3.connect("bugTracker.db")

    #Create database cursor
    c = conn.cursor()

    #Query the database
    c.execute("SELECT oid, * FROM Tickets")
    tickets = c.fetchall()
    #print(tickets)

    #Loop thru results and output them to screen
    print_tickets = ""
    for ticket in tickets:
        print_tickets += str(ticket) + "\n"

    query_label = Label(root, text=print_tickets)
    query_label.grid(row=9, column=0, columnspan=2)


    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

    return

#Create text boxes
ticket_id = Entry(root, width=30)
ticket_id.grid(row=0, column=1, padx=20)
title = Entry(root, width=30)
title.grid(row=1, column=1)
description = Entry(root, width=30)
description.grid(row=2, column=1)
date_created = Entry(root, width=30)
date_created.grid(row=3, column=1)
status = Entry(root, width=30)
status.grid(row=4, column=1)
priority = Entry(root, width=30)
priority.grid(row=5, column=1)
ticket_type = Entry(root, width=30)
ticket_type.grid(row=6, column=1)

#Create text box labels
ticket_id_label = Label(root, text="Ticket ID")
ticket_id_label.grid(row=0, column=0)
title_label = Label(root, text="Title")
title_label.grid(row=1, column=0)
description_label = Label(root, text="Description")
description_label.grid(row=2, column=0)
date_created_label = Label(root, text="Date Created")
date_created_label.grid(row=3, column=0)
status_label = Label(root, text="Status")
status_label.grid(row=4, column=0)
priority_label = Label(root, text="Priority")
priority_label.grid(row=5, column=0)
ticket_type_label = Label(root, text="Ticket Type")
ticket_type_label.grid(row=6, column=0)

#Create submit button
submit_btn = Button(root, text="Submit Ticket", command=submit)
submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

#Create query button
query_btn = Button(root, text="Show All Tickets", command=query)
query_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

#Enter event loop 
root.mainloop()
