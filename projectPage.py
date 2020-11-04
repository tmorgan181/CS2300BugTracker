#Import sqlite3 database tools
import sqlite3

#Import tkinter GUI modules
try:
    from Tkinter import *
    from ttk import *
    from Tkinter import messagebox
except ImportError:  # Python 3
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import messagebox

#Import time functions
from datetime import datetime

###FUNCTIONS###
def Display_Tickets():
    #Connect to database info file
    conn = sqlite3.connect("info.db")
    #Create database cursor
    c = conn.cursor()

    #query the database
    c.execute("SELECT * FROM Tickets WHERE project_ID=?", projID)
    records = c.fetchall()
    #print(records)

    global ticket_table
    ticket_table = Treeview(project_window)
    ticket_table['columns'] = ('ID_num', 'title', 'desc', 'type', 'priority', 'date_created')
    ticket_table['show'] = 'headings'
    ticket_table.heading('ID_num', text='ID #')
    ticket_table.column('ID_num', anchor='center', width=30)
    ticket_table.heading('title', text='Title')
    ticket_table.column('title', anchor='center', width=100)
    ticket_table.heading('desc', text='Description')
    ticket_table.column('desc', anchor='center', width=400)
    ticket_table.heading('type', text='Type')
    ticket_table.column('type', anchor='center', width=50)
    ticket_table.heading('priority', text='Priority')
    ticket_table.column('priority', anchor='center', width=50)
    ticket_table.heading('date_created', text='Created On')
    ticket_table.column('date_created', anchor='center', width=100)
    ticket_table.grid(row=3, columnspan=2, padx=10, sticky = (N,S,W,E))

    for info in records:
        #print(info)
        ticket_table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[5]))

    #Close connection
    conn.close()

    return

def tickMan(ticket_data):
    #Check a ticket has been selected
    if(ticket_data == ''):
        messagebox.showerror("Error", "No ticket selected.")
        project_window.after(1, lambda: project_window.focus_force())
        return

    ticket_ID = str(ticket_data[0])

    #Connect to database info file
    conn = sqlite3.connect("info.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT * FROM Tickets WHERE ticket_ID=?", ticket_ID)
    data = c.fetchone()

    #Open new window
    ticket_manage_window = Toplevel()
    ticket_manage_window.geometry("300x300")
    ticket_manage_window.title("Manage Ticket")

    #Close connection
    conn.close()

    #Place entry box and label for "title" attribute
    title_label = Label(ticket_manage_window, text="Ticket Title*")
    title_label.grid(row=0, column=0, sticky=W, pady=5, padx=5)
    global title_box
    title_box = Entry(ticket_manage_window, width=30)
    title_box.grid(row=1, column=0, columnspan=2, padx=5)
    title_box.insert(END, data[1])

    #Place entry box and label for "description" attribute
    description_label = Label(ticket_manage_window, text="Description")
    description_label.grid(row=2, column=0, sticky=W, pady=5, padx=5)
    global description_box
    description_box = Entry(ticket_manage_window, width=30)
    description_box.grid(row=3, column=0, columnspan=2, padx=5)
    description_box.insert(END, data[2])
    
    #Ticket type and priority labels/menus
    global typeVar
    typeVar = StringVar()
    typeVar.set(str(data[3]))
    newTicketType = Label(ticket_manage_window, text="Type*")
    newTicketType.grid(row=4, column=0, sticky=W, pady=5, padx=5)
    pickType = OptionMenu(ticket_manage_window, typeVar, data[3], "Feature", "Bug")
    pickType.grid(row=5, column=0, sticky=W, padx=5)

    global priorityVar
    priorityVar = StringVar()
    priorityVar.set(str(data[4]))
    newTicketPriority = Label(ticket_manage_window, text="Priority*")
    newTicketPriority.grid(row=6, column=0, sticky=W, pady=5, padx=5)
    pickPriority = OptionMenu(ticket_manage_window, priorityVar, data[4], "Critical", "Major", "Minor", "Trivial")
    pickPriority.grid(row=7, column=0, sticky=W, padx=5)

    #Place buttons for saving changes, cancelling process, and deleting project
    save_btn = Button(ticket_manage_window, text="Save Changes", command=lambda: Save_Changes(ticket_ID, ticket_manage_window))
    save_btn.grid(row=8, column=0, pady=5)
    cancel_btn = Button(ticket_manage_window, text="Cancel", command=lambda: Cancel_Edit(ticket_manage_window))
    cancel_btn.grid(row=8, column=1, pady=5)
    delete_btn = Button(ticket_manage_window, text="Delete Ticket", command=lambda: Delete_Ticket(ticket_ID, ticket_manage_window))
    delete_btn.grid(row=9, column=0, columnspan=2, pady=5)

    return

#Save changes from edited ticket
def Save_Changes(ticket_ID, ticket_manage_window):
    #Connect to database info file
    conn = sqlite3.connect("info.db")
    #Create database cursor
    c = conn.cursor()

    #Update the ticket record
    c.execute("UPDATE Tickets SET title=?, description=?, ticket_type=?, priority=? WHERE ticket_ID=?", (title_box.get(), description_box.get(), typeVar.get(), priorityVar.get(), ticket_ID))
    messagebox.showinfo("Info", "Changes saved.")
    project_window.after(1, lambda: project_window.focus_force())

    #Commit changes
    conn.commit()
    #Close connection
    conn.close()

    #Close the ticket manager
    ticket_manage_window.destroy()

    #Refresh table
    Display_Tickets()

    return

#Cancel changes and close window
def Cancel_Edit(ticket_manage_window):
    #Close the ticket manager
    ticket_manage_window.destroy()

    return

#Delete a ticket from the database
def Delete_Ticket(ticket_ID, ticket_manage_window):
    #Connect to database info file
    conn = sqlite3.connect("info.db")
    #Create database cursor
    c = conn.cursor()

    #Update the ticket record with matching ID
    c.execute("DELETE FROM Tickets WHERE ticket_ID=?", (ticket_ID))
    messagebox.showinfo("Info", "Ticket deleted.")
    project_window.after(1, lambda: project_window.focus_force())

    #Update ticket_count
    c.execute("SELECT ticket_count FROM Projects WHERE project_ID=?", projID)
    count = c.fetchone()[0]
    
    c.execute("UPDATE Projects SET ticket_count=? WHERE project_ID=?", (count-1, projID))

    #Commit changes
    conn.commit()
    #Close connection
    conn.close()

    #Close the ticket manager
    ticket_manage_window.destroy()

    #Refresh tickets table
    Display_Tickets()

    return

def submitTicket(proj_ID):
    global ticketCounter
    #conenct to conn
    conn = sqlite3.connect('info.db')
    #create cursor
    c = conn.cursor()

    curr_date = datetime.now()
    curr_date.isoformat()
    #Only keep YYYY-MM-DD
    curr_date = str(curr_date)[:10]

    #insert into table
    ticket_data = (enterTicketName.get(), enterTicketDescription.get(), clicked1.get(), clicked2.get(), curr_date, proj_ID)
    c.execute("""INSERT INTO Tickets(title, description, ticket_type, priority, date_created, project_ID) VALUES
                (?, ?, ?, ?, ?, ?)""", ticket_data)

    #update ticket count
    c.execute("SELECT ticket_count FROM Projects WHERE project_ID=?", proj_ID)
    count = c.fetchone()[0]

    c.execute("UPDATE Projects SET ticket_count=? WHERE project_ID=?", (count+1, proj_ID))

    #commit changes to conn
    conn.commit()
    #close conn
    conn.close()

    #close create ticket window
    editor.destroy()

    #Refresh tickets table
    Display_Tickets()

    return

#make a new ticket
def tickNew():
    global editor
    global enterTicketName
    global enterTicketDescription
    global pickType
    global pickPriority
    editor = Toplevel()
    editor.title("Create New Ticket")
    editor.geometry("300x300")

    conn = sqlite3.connect("info.db")
    #Create database cursor
    c = conn.cursor()

    #Place entry box and label for "title" attribute
    title_label = Label(editor, text="Ticket Title*")
    title_label.grid(row=0, column=0, sticky=W, pady=5, padx=5)
    enterTicketName = Entry(editor, width=30)
    enterTicketName.grid(row=1, column=0, columnspan=2, padx=5)

    #Place entry box and label for "description" attribute
    description_label = Label(editor, text="Description")
    description_label.grid(row=2, column=0, sticky=W, pady=5, padx=5)
    enterTicketDescription = Entry(editor, width=30)
    enterTicketDescription.grid(row=3, column=0, columnspan=2, padx=5)

    global clicked1
    clicked1 = StringVar()
    clicked1.set("Bug")
    global clicked2
    clicked2 = StringVar()
    clicked2.set("Minor")

    newTicketType = Label(editor, text="Type*")
    newTicketType.grid(row=4, column=0, sticky=W, pady=5, padx=5)
    pickType = OptionMenu(editor, clicked1, "Feature", "Feature", "Bug")
    pickType.grid(row=5, column=0, sticky=W, padx=5)

    newTicketPriority = Label(editor, text="Priority*")
    newTicketPriority.grid(row=6, column=0, sticky=W, pady=5, padx=5)
    pickPriority = OptionMenu(editor, clicked2, "Critical", "Critical", "Major", "Minor", "Trivial")
    pickPriority.grid(row=7, column=0, sticky=W, padx=5)

    submitBtn = Button(editor, text="Create Ticket", command=lambda: submitTicket(projID))
    submitBtn.grid(row=8, column=0, pady=5)

    #Commit changes
    conn.commit()
    #Close connection
    conn.close()

def Count_Tickets(proj_ID):
	#Connect to DB file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Get the count for tickets in the Tickets table
	c.execute("SELECT Count(*) FROM Tickets WHERE project_ID=?", proj_ID)
	ticket_count = c.fetchone()
	#Cursor returns a tuples, so get the first value
	ticket_count = ticket_count[0]

	#Close connection
	conn.close()

	#Return the count
	return ticket_count

#Close window
def Close_Window():
    project_window.destroy()

    return

def View_Project(proj_data):
    #Check a project has been selected
    if(proj_data == ''):
        messagebox.showerror("Error", "No project selected.")
        return

    proj_ID = str(proj_data[0])

    global projID
    projID = proj_ID

    #Open project window
    global project_window
    project_window = Toplevel()
    project_window.geometry("755x425")
    project_window.title("View Project")
    project_window.state("zoomed")

    #conenct to conn
    conn = sqlite3.connect('info.db')
    #create cursor
    c = conn.cursor()

    c.execute("SELECT * FROM Tickets")
    records = c.fetchall()

    global info
    c.execute("SELECT * FROM Projects WHERE project_ID=?", projID)
    info = c.fetchone()
    projectName = info[1]
    projectDescription = info[2]

    #make labels
    projName = Label(project_window, text=str(projectName))
    projName.config(font=("", 24, "bold"))
    projName.grid(row=0, column=0, columnspan=2)
    projDescription = Label(project_window, text=str(projectDescription))
    projDescription.grid(row=1, column=0, columnspan=2)
    ticketTitle = Label(project_window, text="Project Tickets")
    ticketTitle.config(font="TkDefaultFont 9 underline")
    ticketTitle.grid(row=2, column=0, pady=5, padx=10, sticky=W)
	
    Display_Tickets()

    manage_tick_btn = Button(project_window, text="Manage Ticket", command=lambda: tickMan(ticket_table.item(ticket_table.focus())['values']))
    manage_tick_btn.grid(row=5, column=0, columnspan=2, pady=5)

    #Place "Create New Ticket" button
    create_ticket_btn = Button(project_window, text="Create New Ticket", command=tickNew)
    create_ticket_btn.grid(row=6, column=0, columnspan=2)

    #Place "Back" button
    back_btn = Button(project_window, text="Back", command=Close_Window)
    back_btn.grid(row=7, column=1, sticky=E, padx=10, pady=5)

    #Close connection
    conn.close()

    return