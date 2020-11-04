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

#Import project page code
import projectPage

###INITIALIZE DATABASE###
def Init_Database():
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#All tables are created only on the first run of the app
	#Create Ticket table
	try:
		c.execute("""
		CREATE TABLE Tickets (
		ticket_ID Integer PRIMARY KEY,
		title Text,
		description Text,
		ticket_type Text,
		priority Text,
		date_created Text,
		project_ID Integer,
		FOREIGN KEY (project_ID) REFERENCES Projects(project_ID)
		ON DELETE CASCADE
		)
		""")

		print("Table \'Tickets\' successfully created")

	except(sqlite3.OperationalError):
		print("Table \'Tickets\' already exists")

	#Create Projects table
	try:
		c.execute("""
			CREATE TABLE Projects (
			project_ID Integer PRIMARY KEY,
			name Text,
			description Text,
			ticket_count Integer,
			date_created Text
			)
			""")

		print("Table \'Projects\' successfully created")

	except(sqlite3.OperationalError):
		print("Table \'Projects\' already exists")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	return

###CREATE HOMEPAGE###
def Homepage():
	#Create root window
	global root
	root = Tk()
	root.title("Bug Tracker")
	root.geometry("755x450")
	root.state("zoomed")

	#Place title frame
	title_frame = Frame(root, height=10, width=500)
	title_frame.grid(row=0, column=0, columnspan=2, pady=5)
	title_label = Label(title_frame, text="Welcome to the Bug Tracker!")
	title_label.config(font=("", 24, "bold"))
	title_label.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)

	#Place "Your Projects" label
	your_proj_label = Label(root, text="Your Projects")
	your_proj_label.configure(font="TkDefaultFont 9 underline")
	your_proj_label.grid(row=1, column=0, pady=5, padx=10, sticky=W)

	#Display projects
	Display_Projects()

	view_proj_btn = Button(root, text="View Project", command=lambda: projectPage.View_Project(project_table.item(project_table.focus())['values']))
	view_proj_btn.grid(row=4, column=0, columnspan=2, pady=5)
	manage_proj_btn = Button(root, text="Manage Project", command=lambda: Manage_Project(project_table.item(project_table.focus())['values']))
	manage_proj_btn.grid(row=5, column=0, columnspan=2)

	#Place "Create New Project" button
	create_proj_btn = Button(root, text="Create New Project", command=Create_Project)
	create_proj_btn.grid(row=6, column=0, columnspan=2, pady=5)

	#Place "See All" button
	see_all_btn = Button(root, text="See All Tickets", command=See_All)
	see_all_btn.grid(row=7, column=0, sticky=W, padx=10, pady=5)

	#Place "Exit" button
	exit_btn = Button(root, text="Exit", command=lambda: root.destroy())
	exit_btn.grid(row=7, column=1, sticky=E, padx=10, pady=5)

	#Start event loop
	root.mainloop()

	return

###HELPER FUNCTIONS###
#Count the total number of projects present in the database
def Count_Projects():
	#Connect to DB file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Get the count for projects in the Projects table
	c.execute("SELECT Count(*) FROM Projects")
	proj_count = c.fetchone()
	#Cursor returns a tuples, so get the first value
	proj_count = proj_count[0]

	#Close connection
	conn.close()

	#Return the count
	return proj_count

#Display projects in a table
def Display_Projects():
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Get a list of all current project IDs
	c.execute("SELECT project_ID FROM Projects")
	ID_list = c.fetchall()
	#print(ID_list)

	#Display projects within a table
	global project_table
	project_table = Treeview(root)
	project_table['columns'] = ('ID_num', 'name', 'desc', 'tickets', 'date_created')
	project_table['show'] = 'headings'
	project_table.heading('ID_num', text='ID #')
	project_table.column('ID_num', anchor='center', width=30)
	project_table.heading('name', text='Name')
	project_table.column('name', anchor='center', width=100)
	project_table.heading('desc', text='Description')
	project_table.column('desc', anchor='center', width=400)
	project_table.heading('tickets', text='Ticket Count')
	project_table.column('tickets', anchor='center', width=100)
	project_table.heading('date_created', text='Created On')
	project_table.column('date_created', anchor='center', width=100)
	project_table.grid(row=2, columnspan=2, padx=10, sticky = (N,S,W,E))

	for x in ID_list:
		c.execute("SELECT * FROM Projects WHERE project_ID=?", x)
		info = c.fetchone()
		#print(info)
		project_table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4]))

	#Close connection
	conn.close()

###BUTTON FUNCTIONS###
#Create a new project and insert it into the database
def Create_Project():
	#Open new window
	proj_window = Toplevel()
	proj_window.geometry("300x300")
	proj_window.title("Create New Project")

	#Place entry box and label for "name" attribute
	name_label = Label(proj_window, text="Project Name*")
	name_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
	name_box = Entry(proj_window, width=30)
	name_box.grid(row=2, column=0, padx=5)

	#Place entry box and label for "description" attribute
	description_label = Label(proj_window, text="Description")
	description_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
	description_box = Entry(proj_window, width=30)
	description_box.grid(row=4, column=0, padx=5)

	#Place submit button
	submit_btn = Button(proj_window, text="Create Project", command=lambda: Submit_Project(name_box, description_box, proj_window))
	submit_btn.grid(row=5, column=0, pady=5)

	return

#Insert a project with the given field values into the Projects table
def Submit_Project(name_box, description_box, proj_window):
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Get the current date
	curr_date = datetime.now()
	curr_date.isoformat()
	#Only keep YYYY-MM-DD
	curr_date = str(curr_date)[:10]

	#Insert the new project
	proj_data = (name_box.get(), description_box.get(), 0, curr_date)
	c.execute("""INSERT INTO Projects(name, description, ticket_count, date_created) VALUES
				(?, ?, ?, ?)""", proj_data)

	#Close proj_window
	proj_window.destroy()

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Refresh Table
	Display_Projects()

	return

#Open project manager window to allow deletion and editing of projects
def Manage_Project(proj_data):
	#Check a project has been selected
	if(proj_data == ''):
		messagebox.showerror("Error", "No project selected.")
		return

	proj_ID = str(proj_data[0])

	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	c.execute("SELECT * FROM Projects WHERE project_ID=?", proj_ID)
	data = c.fetchone()
	
	#Close connection
	conn.close()

	#Open new window
	proj_manage_window = Toplevel()
	proj_manage_window.geometry("300x300")
	proj_manage_window.title("Manage Project")

	#Place entry box and label for "name" attribute
	name_label = Label(proj_manage_window, text="Project Name*")
	name_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
	name_box = Entry(proj_manage_window, width=30)
	name_box.insert(END, data[1])
	name_box.grid(row=2, column=0, columnspan=2, padx=5)

	#Place entry box and label for "description" attribute
	description_label = Label(proj_manage_window, text="Description")
	description_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
	description_box = Entry(proj_manage_window, width=30)
	description_box.insert(END, data[2])
	description_box.grid(row=4, column=0, columnspan=2, padx=5)

	#Place buttons for saving changes, cancelling process, and deleting project
	save_btn = Button(proj_manage_window, text="Save Changes", command=lambda: Save_Changes(proj_ID, name_box, description_box, proj_manage_window))
	save_btn.grid(row=5, column=0, pady=5)
	cancel_btn = Button(proj_manage_window, text="Cancel", command=lambda: Cancel_Edit(proj_manage_window))
	cancel_btn.grid(row=5, column=1, pady=5)
	delete_btn = Button(proj_manage_window, text="Delete Project", command=lambda: Delete_Project(proj_ID, proj_manage_window))
	delete_btn.grid(row=6, column=0, columnspan=2, pady=5)

	return

#Save changes from edited project
def Save_Changes(proj_ID, name_box, description_box, proj_manage_window):
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Update the project record with matching proj_ID
	c.execute("UPDATE Projects SET name=?, description=? WHERE project_ID=?", (name_box.get(), description_box.get(), proj_ID))
	messagebox.showinfo("Info", "Changes saved.")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the project manager
	proj_manage_window.destroy()

	#Refresh Table
	Display_Projects()

	return

#Cancel changes and close window
def Cancel_Edit(proj_manage_window):
	#Close the project manager
	proj_manage_window.destroy()

	return

#Delete a project from the database
def Delete_Project(proj_ID, proj_manage_window):
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Delete all tickets associated with project
	c.execute("DELETE FROM Tickets WHERE project_ID=?", proj_ID)

	#Update the project record with matching proj_ID
	c.execute("DELETE FROM Projects WHERE project_ID=?", proj_ID)
	messagebox.showinfo("Info", "Project deleted.")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the project manager
	proj_manage_window.destroy()

	#Refresh Table
	Display_Projects()

	return

#See all projects and tickets (table union)
def See_All():
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Ensure a project and a ticket exist
	c.execute("SELECT Count(*) FROM Tickets")
	count = c.fetchone()

	if(count[0] == 0):
		messagebox.showerror("Error", "No tickets to display.")
		return

	#Open new window
	global see_all_window
	see_all_window = Toplevel()
	see_all_window.title("All Data")
	see_all_window.geometry("755x450")
	see_all_window.state("zoomed")

	#"All Tickets" label
	all_tickets = Label(see_all_window, text="All Tickets In Database")
	all_tickets.configure(font="TkDefaultFont 9 underline")
	all_tickets.grid(row=1, column=0, pady=5, padx=10, sticky=W)

	#Display projects within a table
	global see_all_table
	see_all_table = Treeview(see_all_window)
	see_all_table['columns'] = ('ticket_ID', 'ticket_title', 'project_name', 'date_created')
	see_all_table['show'] = 'headings'
	see_all_table.heading('ticket_ID', text='ID #', command=lambda: Sort_Column(see_all_table, 'ticket_ID', False))
	see_all_table.column('ticket_ID', anchor='center', width=50)
	see_all_table.heading('ticket_title', text='Ticket Title', command=lambda: Sort_Column(see_all_table, 'ticket_title', False))
	see_all_table.column('ticket_title', anchor='center', width=265)
	see_all_table.heading('project_name', text='Project Name', command=lambda: Sort_Column(see_all_table, 'project_name', False))
	see_all_table.column('project_name', anchor='center', width=265)
	see_all_table.heading('date_created', text='Created On', command=lambda: Sort_Column(see_all_table, 'date_created', False))
	see_all_table.column('date_created', anchor='center', width=200)
	see_all_table.grid(row=2, columnspan=2, padx=10, sticky = (N,S,W,E))

	#Get a list of all current ticket IDs
	c.execute("SELECT ticket_ID FROM Tickets")
	ID_list = c.fetchall()
	#print(ID_list)

	c.execute("""SELECT Tickets.ticket_ID, Tickets.title, Projects.name, Tickets.date_created 
			FROM Tickets INNER JOIN Projects ON Tickets.project_ID=Projects.project_ID
			""")

	count = 0
	for x in ID_list:
		info = c.fetchone()
		#print(info)
		see_all_table.insert("", "end", values=(info[0], info[1], info[2], info[3]))
		count +=1

	#total tickets label
	message = "Total Tickets: " + str(count)
	total = Label(see_all_window, text=message)
	total.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky=W+E)

	#Ticket search bar
	search_bar_label = Label(see_all_window, text="Search by ticket title:")
	search_bar_label.grid(row=4, column=0, pady=5, sticky=E)

	search_bar = Entry(see_all_window, width=30)
	search_bar.grid(row=4, column=1, pady=5, padx=10, sticky=W)

	sumbit_search = Button(see_all_window, text="Search", command=lambda: Search_Ticket(search_bar.get()))
	sumbit_search.grid(row=5, column=0, columnspan=2, pady=5)

	#Place "Back" button
	back_btn = Button(see_all_window, text="Back", command=lambda: see_all_window.destroy())
	back_btn.grid(row=6, column=1, sticky=E, padx=10, pady=5)

	return

#Sort the table by column
def Sort_Column(table, column, reverse):
	l = [(table.set(k, column), k) for k in table.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
	    table.move(k, '', index)

	# reverse sort next time
	table.heading(column, command=lambda: Sort_Column(see_all_table, column, not reverse))

	return

#Search for a ticket by title and show details
def Search_Ticket(title):
	title = str(title)
	#print("searching for ticket with title: " + title)

	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Check if ticket with matching title exists
	c.execute("SELECT Count(*) FROM Tickets WHERE title=?", (title,))
	count = c.fetchone()

	if(count[0] == 0):
		messagebox.showerror("Error", "No ticket with title \'" + title + "\'.")
		see_all_window.after(1, lambda: see_all_window.focus_force())
		return

	#Display details in new window
	ticket_details = Toplevel()
	ticket_details.title("Ticket Details")
	ticket_details.geometry("400x400")

	c.execute("""SELECT Tickets.ticket_ID, Tickets.title, Tickets.description, Projects.name, Tickets.ticket_type, Tickets.priority, Tickets.date_created 
			FROM Tickets INNER JOIN Projects ON Tickets.project_ID=Projects.project_ID WHERE Tickets.title=?""", (title,))
	data = c.fetchone()

	#Close connection
	conn.close()

	#ID attribute
	ID_label = Label(ticket_details, text="Ticket ID #")
	ID_label.grid(row=0, column=0, sticky=W, pady=5, padx=5)
	ID_box = Entry(ticket_details, width=5)
	ID_box.grid(row=1, column=0, columnspan=2, padx=5, sticky=W)
	ID_box.insert(0, data[0])
	ID_box.config(state='readonly')

	#Title attribute
	title_label = Label(ticket_details, text="Ticket Title")
	title_label.grid(row=2, column=0, sticky=W, pady=5, padx=5)
	title_box = Entry(ticket_details, width=30)
	title_box.grid(row=3, column=0, columnspan=2, padx=5, sticky=W)
	title_box.insert(0, data[1])
	title_box.config(state='readonly')

	#Description attribute
	description_label = Label(ticket_details, text="Description")
	description_label.grid(row=4, column=0, sticky=W, pady=5, padx=5)
	description_box = Entry(ticket_details, width=50)
	description_box.grid(row=5, column=0, columnspan=2, padx=5, sticky=W)
	description_box.insert(0, data[2])
	description_box.config(state='readonly')

	#Project name attribute
	project_label = Label(ticket_details, text="Parent Project Name")
	project_label.grid(row=6, column=0, sticky=W, pady=5, padx=5)
	project_box = Entry(ticket_details, width=30)
	project_box.grid(row=7, column=0, columnspan=2, padx=5, sticky=W)
	project_box.insert(0, data[3])
	project_box.config(state='readonly')

	#Ticket type attribute
	type_label = Label(ticket_details, text="Ticket Type")
	type_label.grid(row=8, column=0, sticky=W, pady=5, padx=5)
	type_box = Entry(ticket_details, width=10)
	type_box.grid(row=9, column=0, columnspan=2, padx=5, sticky=W)
	type_box.insert(0, data[4])
	type_box.config(state='readonly')

	#Ticket priority attribute
	priority_label = Label(ticket_details, text="Ticket Priority")
	priority_label.grid(row=10, column=0, sticky=W, pady=5, padx=5)
	priority_box = Entry(ticket_details, width=10)
	priority_box.grid(row=11, column=0, columnspan=2, padx=5, sticky=W)
	priority_box.insert(0, data[5])
	priority_box.config(state='readonly')

	#Creation date attribute
	date_label = Label(ticket_details, text="Date Created")
	date_label.grid(row=12, column=0, sticky=W, pady=5, padx=5)
	date_box = Entry(ticket_details, width=20)
	date_box.grid(row=13, column=0, columnspan=2, padx=5, sticky=W)
	date_box.insert(0, data[6])
	date_box.config(state='readonly')

	#Close button
	close_btn = Button(ticket_details, text="Close", command=lambda: ticket_details.destroy())
	close_btn.grid(row=14, column=1, padx=10, pady=10, sticky=S+E)

	return