#Import sqlite3 database tools
import sqlite3

#Import tkinter GUI modules
try:
	from Tkinter import *
	from ttk import *
except ImportError:  # Python 3
	from tkinter import *
	from tkinter.ttk import *

#Import time functions
from datetime import datetime

###FUNCTIONS###
def tickMan():
	#Open new window
	ticket_manage_window = Toplevel()
	ticket_manage_window.geometry("300x300")
	ticket_manage_window.title("Manage Ticket")

	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Ensure project exists
	c.execute("SELECT Count(*) FROM Tickets WHERE ticket_ID=?", (ticket_ID,))
	count = str(c.fetchone()[0])
	if (count == "0"):
		print("Ticket does not exist")
		return

	#Close connection
	conn.close()

	#Place entry box and label for "title" attribute
	title_label = Label(ticket_manage_window, text="Ticket Title*")
	title_label.grid(row=0, column=0, sticky=W)
	global title_box
	title_box = Entry(ticket_manage_window, width=30)
	title_box.grid(row=1, column=0, columnspan=2)

	#Place entry box and label for "description" attribute
	description_label = Label(ticket_manage_window, text="Description")
	description_label.grid(row=2, column=0, sticky=W)
	global description_box
	description_box = Entry(ticket_manage_window, width=30)
	description_box.grid(row=3, column=0, columnspan=2)
	
	#Ticket type and priority labels/menus
	global typeVar
	typeVar = StringVar()
	typeVar.set("Bug")
	newTicketType = Label(ticket_manage_window, text="Type*")
	newTicketType.grid(row=4, column=0, sticky=W)
	pickType = OptionMenu(ticket_manage_window, typeVar, "Feature", "Feature", "Bug")
	pickType.grid(row=5, column=0, sticky=W)

	global priorityVar
	priorityVar = StringVar()
	priorityVar.set("Minor")
	newTicketPriority = Label(ticket_manage_window, text="Priority*")
	newTicketPriority.grid(row=6, column=0, sticky=W)
	pickPriority = OptionMenu(ticket_manage_window, priorityVar, "Critical", "Critical", "Major", "Minor", "Trivial")
	pickPriority.grid(row=7, column=0, sticky=W)

	#Place buttons for saving changes, cancelling process, and deleting project
	save_btn = Button(ticket_manage_window, text="Save Changes", command=lambda: Save_Changes(ticket_ID, ticket_manage_window))
	save_btn.grid(row=8, column=0)
	cancel_btn = Button(ticket_manage_window, text="Cancel", command=lambda: Cancel_Edit(ticket_manage_window))
	cancel_btn.grid(row=8, column=1)
	delete_btn = Button(ticket_manage_window, text="Delete Ticket", command=lambda: Delete_Ticket(ticket_ID, ticket_manage_window))
	delete_btn.grid(row=9, column=0, columnspan=2)

	return

#Save changes from edited ticket
def Save_Changes(ticket_ID, ticket_manage_window):
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Update the ticket record
	c.execute("UPDATE Tickets SET title=?, description=?, ticket_type=?, priority=? WHERE ticket_ID=?", (title_box.get(), description_box.get(), typeVar.get(), priorityVar.get(), ticket_ID))
	print("Changes saved")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the ticket manager
	ticket_manage_window.destroy()

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
	print("Ticket deleted")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the ticket manager
	ticket_manage_window.destroy()

	return

#entry_text = StringVar()
#dayValue.trace('w', limitSizeDay)
ticketCounter = 0
def submitTicket(proj_ID):
	global ticketCounter
	#conenct to conn
	conn = sqlite3.connect('info.db')
	#create cursor
	c = conn.cursor()

	ticketStatus = "In Progress"

	curr_date = datetime.now()
	curr_date.isoformat()
	#Only keep YYYY-MM-DD
	curr_date = str(curr_date)[:10]

	ticket_data = (enterTicketName.get(), enterTicketDescription.get(), clicked1.get(), clicked2.get(), ticketStatus, curr_date, proj_ID)
	c.execute("""INSERT INTO Tickets(title, description, ticket_type, priority, status, date_created, project_ID) VALUES
				(?, ?, ?, ?, ?, ?, ?)""", ticket_data)

	c.execute("SELECT * FROM Tickets WHERE project_ID=?", proj_ID)
	records = c.fetchall()
	#print(records)

	#Configure table
	table = Treeview(project_window)
	table['columns'] = ('ID_num', 'title', 'desc', 'type', 'priority', 'date_created')
	table['show'] = 'headings'
	table.heading('ID_num', text='ID #')
	table.column('ID_num', anchor='center', width=30)
	table.heading('title', text='Title')
	table.column('title', anchor='center', width=100)
	table.heading('desc', text='Description')
	table.column('desc', anchor='center', width=250)
	table.heading('type', text='Type')
	table.column('type', anchor='center', width=50)
	table.heading('priority', text='Priority')
	table.column('priority', anchor='center', width=50)
	table.heading('date_created', text='Created On')
	table.column('date_created', anchor='center', width=100)
	table.grid(row=6, columnspan=3, sticky = (N,S,W,E))

	for info in records:
		#print(info)
		table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[6]))

		editor.destroy()

	#commit changes to conn
	conn.commit()

	#close conn
	conn.close()

#make a new ticket
def tickNew():
	global editor
	global enterTicketName
	global enterTicketDescription
	global pickType
	global pickPriority
	editor = Toplevel()
	editor.title("New Ticket")
	editor.geometry("400x400")
	
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#old labels and entries
	'''newTicketName = Label(editor, text="Title (required)")
	newTicketName.grid(row=0, column=0)
	newTicketDescription = Label(editor, text="Description")
	newTicketDescription.grid(row=2, column=0)
	newTicketType = Label(editor, text="Type (required)")
	newTicketType.grid(row=4, column=0)
	newTicketPriority = Label(editor, text="Priority (required)")
	newTicketPriority.grid(row=6, column=0)
	enterTicketName = Entry(editor, width=30)
	enterTicketName.grid(row=1, column=0, padx=15, pady=(0,10))
	enterTicketDescription = Entry(editor, width=30)
	enterTicketDescription.grid(row=3, column=0, padx=15, pady=(0,10))'''

	#Place entry box and label for "title" attribute
	title_label = Label(editor, text="Ticket Title*")
	title_label.grid(row=0, column=0, sticky=W)
	enterTicketName = Entry(editor, width=30)
	enterTicketName.grid(row=1, column=0, columnspan=2)

	#Place entry box and label for "description" attribute
	description_label = Label(editor, text="Description")
	description_label.grid(row=2, column=0, sticky=W)
	enterTicketDescription = Entry(editor, width=30)
	enterTicketDescription.grid(row=3, column=0, columnspan=2)

	global clicked1
	clicked1 = StringVar()
	clicked1.set("Bug")
	global clicked2
	clicked2 = StringVar()
	clicked2.set("Minor")

	
	pickType = OptionMenu(editor, clicked1, "Feature", "Feature", "Bug")
	pickType.grid(row=5, column=0, pady=(0,10))
	pickPriority = OptionMenu(editor, clicked2, "Critical", "Critical", "Major", "Minor", "Trivial")
	pickPriority.grid(row=7, column=0, pady=(0,10))

	submitBtn = Button(editor, text="Create ticket", command=lambda: submitTicket(projID))
	submitBtn.grid(row=8, column=0, pady=(10,0))

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

def View_Project(proj_ID):
	global projID
	projID = proj_ID

	#conenct to conn
	conn = sqlite3.connect('info.db')
	#create cursor
	c = conn.cursor()

	c.execute("SELECT * FROM Projects")
	records = c.fetchall()
	cont = 0
	for x in records:
		if int(x[0]) == int(projID):
			print("project does exist")
			cont = 1
			break

	if(cont == 0):
		print("project does not exist")
		return
	#Open project window
	global project_window
	project_window = Toplevel()
	project_window.geometry("600x400")
	project_window.title("View Project")

	#c.execute("SELECT * FROM Tickets")
	#records = c.fetchall()

	global info
	c.execute("SELECT * FROM Projects WHERE project_ID=?", projID)
	info = c.fetchone()
	projectName = str(info[1])
	projectDescription = str(info[2])


	#make (old) labels
	'''projName = Label(project_window, text=str(projectName))
	projName.config(font=("", 16))
	projName.grid(row=0, column=1, columnspan=2, padx=(0,100), pady=(10,0))
	projDescription = Label(project_window, text=str(projectDescription))
	projDescription.config(font=("", 10))
	projDescription.grid(row=2, column=0, padx=(20,0))
	ticketTitle = Label(project_window, text="Tickets")
	ticketTitle.config(font=("", 16))
	ticketTitle.grid(row=3, column=1, pady=(15,0), padx=(25,0))
	#make buttons
	manageTicket = Button(project_window, text="Manage Ticket", command=tickMan)
	manageTicket.grid(row=1, column=2)
	createTicket = Button(project_window, text="Create Ticket", command=tickNew)
	createTicket.grid(row=5, column=1, pady=(10,0))'''
	
	#make labels
	projName = Label(project_window, text=str(projectName))
	#projName.config(font=("", 16))
	projName.grid(row=0, column=0, columnspan=2)
	projDescription = Label(project_window, text=str(projectDescription))
	#projDescription.config(font=("", 12))
	projDescription.grid(row=1, column=0, columnspan=2)
	ticketTitle = Label(project_window, text="Project Tickets")
	ticketTitle.config(font="TkDefaultFont 9 underline")
	ticketTitle.grid(row=2, column=0, sticky=W)

	create_tick_btn = Button(project_window, text="Create New Ticket", command=tickNew)
	create_tick_btn.grid(row=7, column=0, columnspan=2)

	ticket_count = Count_Tickets(proj_ID)
	if (ticket_count == 0):
		#Display "No Tickets Found" instead of table
		no_ticket_label = Label(project_window, text="No Tickets Found")
		no_ticket_label.grid(row=3, column=0, columnspan=2)
	else:
		Display_Tickets(proj_ID)

		#Create field to manage a certain ticket
		select_label = Label(project_window, text="Ticket ID Number:")
		select_label.grid(row=4, column=0, sticky=E)
		ticket_select_box = Entry(project_window, width=30)
		ticket_select_box.grid(row=4, column=1)

		manage_tick_btn = Button(project_window, text="Manage Ticket", command=lambda: tickMan(ticket_select_box.get()))
		manage_tick_btn.grid(row=5, column=0, columnspan=2)

		#Place "Create New Ticket" button
		

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	return

def Display_Tickets(proj_ID):
	#conenct to conn
	conn = sqlite3.connect('info.db')
	#create cursor
	c = conn.cursor()

	#query the database
	c.execute("SELECT * FROM Tickets WHERE project_ID=?", proj_ID)
	records = c.fetchall()
	#print(records)

	#Configure table
	table = Treeview(project_window)
	table['columns'] = ('ID_num', 'title', 'desc', 'type', 'priority', 'date_created')
	table['show'] = 'headings'
	table.heading('ID_num', text='ID #')
	table.column('ID_num', anchor='center', width=30)
	table.heading('title', text='Title')
	table.column('title', anchor='center', width=100)
	table.heading('desc', text='Description')
	table.column('desc', anchor='center', width=250)
	table.heading('type', text='Type')
	table.column('type', anchor='center', width=50)
	table.heading('priority', text='Priority')
	table.column('priority', anchor='center', width=50)
	table.heading('date_created', text='Created On')
	table.column('date_created', anchor='center', width=100)
	table.grid(row=6, columnspan=3, sticky = (N,S,W,E))

	for info in records:
		#print(info)
		table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[6]))

	#close conn
	conn.close()

	return