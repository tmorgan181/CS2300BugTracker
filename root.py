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

#Flag indicates whether or not to populate the database tables with example data on creation
populate_tables = "False"

###INITIALIZE DATABASE###
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

###EXAMPLE SET INSERTION###
#Example set to be used for demonstration
#TBD

#Populate function uses the given example data to be inserted into the database after initialization
def populate():
	print("Populate Function Called")
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
	see_all_window = Toplevel()
	see_all_window.title("All Data")
	see_all_window.geometry("755x450")

	#"All Tickets" label
	all_tickets = Label(see_all_window, text="All Tickets In Database")
	all_tickets.configure(font="TkDefaultFont 9 underline")
	all_tickets.grid(row=1, column=0, pady=5, padx=10, sticky=W)

	#Display projects within a table
	see_all_table = Treeview(see_all_window)
	see_all_table['columns'] = ('ticket_ID', 'ticket_title', 'project_name', 'type', 'priority', 'date_created')
	see_all_table['show'] = 'headings'
	see_all_table.heading('ticket_ID', text='ID #')
	see_all_table.column('ticket_ID', anchor='center', width=50)
	see_all_table.heading('ticket_title', text='Ticket Title')
	see_all_table.column('ticket_title', anchor='center', width=200)
	see_all_table.heading('project_name', text='Project Name')
	see_all_table.column('project_name', anchor='center', width=200)
	see_all_table.heading('type', text='Type')
	see_all_table.column('type', anchor='center', width=50)
	see_all_table.heading('priority', text='Priority')
	see_all_table.column('priority', anchor='center', width=50)
	see_all_table.heading('date_created', text='Created On')
	see_all_table.column('date_created', anchor='center', width=100)
	see_all_table.grid(row=2, columnspan=2, padx=10, sticky = (N,S,W,E))

	#Get a list of all current ticket IDs
	c.execute("SELECT ticket_ID FROM Tickets")
	ID_list = c.fetchall()
	#print(ID_list)

	c.execute("""SELECT Tickets.ticket_ID, Tickets.title, Projects.name, Tickets.ticket_type, Tickets.priority, Tickets.date_created 
			FROM Tickets INNER JOIN Projects ON Tickets.project_ID=Projects.project_ID
			""")

	count = 0
	for x in ID_list:
		info = c.fetchone()
		#print(info)
		see_all_table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[5]))
		count +=1

	#total tickets label
	message = "Total Tickets: " + str(count)
	total = Label(see_all_window, text=message)
	total.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky=W+E)

	return

#Close application
def Close_App():
	root.destroy()

	return

###CREATE HOMEPAGE###
def Homepage():
	#Create root window
	global root
	root = Tk()
	root.title("Bug Tracker")
	root.geometry("755x450")

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
	proj_count = Count_Projects()
	if (proj_count == 0):
		#Display "No Projects Found" instead of buttons
		no_proj_label = Label(root, text="No Projects Found")
		no_proj_label.grid(row=2, column=0, columnspan=2)
	else:
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
	exit_btn = Button(root, text="Exit", command=Close_App)
	exit_btn.grid(row=7, column=1, sticky=E, padx=10, pady=5)

	#Close connection
	conn.close()

	return

#Initialize app
Homepage()
root.mainloop()