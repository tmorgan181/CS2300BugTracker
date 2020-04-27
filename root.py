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
		status Text,
		date_created Text,
		project_ID Integer,
		FOREIGN KEY (project_ID) REFERENCES Projects(project_ID)
			ON DELETE CASCADE
		)
		""")
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

#Generate a button for the project with ID 'proj_ID'
def Generate_Button(proj_ID):
	#Connect to DB file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Select the project tuple with matching ID
	c.execute("SELECT * FROM Projects WHERE project_ID = ?", (proj_ID,))
	proj_info = c.fetchone()
	print(proj_info)

	#Create frame for the project info
	proj_frame = Frame(root, width=300, height=100)
	#Disable resizing of frame
	proj_frame.grid_propagate(False)
	#Enable button to fill frame
	proj_frame.columnconfigure(0, weight=1)
	proj_frame.rowconfigure(0, weight=1)
	proj_frame.grid(columnspan=2)

	#Create and place button
	btn_text = str(proj_info[0]) + "\t\t" + str(proj_info[1])
	proj_btn = Button(proj_frame, text=btn_text, command=lambda: projectPage.View_Project(proj_ID))
	proj_btn.grid(row=0, column=0)

	#Place description beneath button
	desc_label = Label(proj_frame, text="-- " + proj_info[2])
	desc_label.grid(row=1, column=0, sticky=N+W)

	#Close connection
	conn.close()

	return

###BUTTON FUNCTIONS###
#Create a new project and insert it into the database
def Create_Project():
	#Open new window
	proj_window = Toplevel()
	proj_window.geometry("300x300")
	proj_window.title("Create New Project")

	#Place entry box and label for "name" attribute
	name_label = Label(proj_window, text="Project Name*")
	name_label.grid(row=1, column=0, sticky=W)
	name_box = Entry(proj_window, width=30)
	name_box.grid(row=2, column=0)

	#Place entry box and label for "description" attribute
	description_label = Label(proj_window, text="Description")
	description_label.grid(row=3, column=0, sticky=W)
	description_box = Entry(proj_window, width=30)
	description_box.grid(row=4, column=0)

	#Place submit button
	submit_btn = Button(proj_window, text="Create Project", command=lambda: Submit_Project(name_box, description_box, proj_window))
	submit_btn.grid(row=5, column=0)

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

	return

#Open project manager window to allow deletion and editing of projects
def Manage_Project(proj_ID):
	#Open new window
	proj_manage_window = Toplevel()
	proj_manage_window.geometry("300x300")
	proj_manage_window.title("Manage Project")

	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Ensure project exists
	c.execute("SELECT Count(*) FROM Projects WHERE project_ID=?", (proj_ID,))
	count = str(c.fetchone()[0])
	if (count == "0"):
		print("Project does not exist")
		return

	#Close connection
	conn.close()

	#Place entry box and label for "name" attribute
	name_label = Label(proj_manage_window, text="Project Name*")
	name_label.grid(row=1, column=0, sticky=W)
	name_box = Entry(proj_manage_window, width=30)
	name_box.grid(row=2, column=0, columnspan=2)

	#Place entry box and label for "description" attribute
	description_label = Label(proj_manage_window, text="Description")
	description_label.grid(row=3, column=0, sticky=W)
	description_box = Entry(proj_manage_window, width=30)
	description_box.grid(row=4, column=0, columnspan=2)

	#Place buttons for saving changes, cancelling process, and deleting project
	save_btn = Button(proj_manage_window, text="Save Changes", command=lambda: Save_Changes(proj_ID, name_box, description_box, proj_manage_window))
	save_btn.grid(row=5, column=0)
	cancel_btn = Button(proj_manage_window, text="Cancel", command=lambda: Cancel_Edit(proj_manage_window))
	cancel_btn.grid(row=5, column=1)
	delete_btn = Button(proj_manage_window, text="Delete Project", command=lambda: Delete_Project(proj_ID, proj_manage_window))
	delete_btn.grid(row=6, column=0, columnspan=2)

	return

#Save changes from edited project
def Save_Changes(proj_ID, name_box, description_box, proj_manage_window):
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Update the project record with matching proj_ID
	c.execute("UPDATE Projects SET name=?, description=? WHERE project_ID=?", (name_box.get(), description_box.get(), proj_ID))
	print("Changes saved")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the project manager
	proj_manage_window.destroy()

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

	#Update the project record with matching proj_ID
	c.execute("DELETE FROM Projects WHERE project_ID=?", (proj_ID))
	print("Project deleted")

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	#Close the project manager
	proj_manage_window.destroy()

	return

###CREATE HOMEPAGE###
#Create root window
root = Tk()
root.title("Bug Tracker")
root.geometry("500x500")

#Place title frame
title_frame = Frame(root, height=10, width=500)
title_frame.grid(row=0, column=0, columnspan=2, pady=5)
title_label = Label(title_frame, text="Welcome to the Bug Tracker!")
title_label.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)

#Place "Your Projects" label
your_proj_label = Label(root, text="Your Projects")
your_proj_label.configure(font="TkDefaultFont 9 underline")
your_proj_label.grid(row=1, column=0, columnspan=2, pady=5, sticky=W)

#Generate and place buttons for each of the user's projects
proj_count = Count_Projects()
if (proj_count == 0):
	#Display "No Projects Found" instead of buttons
	no_proj_label = Label(root, text="No Projects Found")
	no_proj_label.grid(row=2, column=0, columnspan=2)
else:
	#Connect to database info file
	conn = sqlite3.connect("info.db")
	#Create database cursor
	c = conn.cursor()

	#Get a list of all current project IDs
	c.execute("SELECT project_ID FROM Projects")
	ID_list = c.fetchall()
	print(ID_list)

	#Display projects within a table
	table = Treeview(root)
	table['columns'] = ('ID_num', 'name', 'desc', 'tickets', 'date_created')
	table['show'] = 'headings'
	table.heading('ID_num', text='ID #')
	table.column('ID_num', anchor='center', width=30)
	table.heading('name', text='Name')
	table.column('name', anchor='center', width=100)
	table.heading('desc', text='Description')
	table.column('desc', anchor='center', width=250)
	table.heading('tickets', text='Ticket Count')
	table.column('tickets', anchor='center', width=100)
	table.heading('date_created', text='Created On')
	table.column('date_created', anchor='center', width=100)
	table.grid(row=2, columnspan=2, sticky = (N,S,W,E))

	for x in ID_list:
		c.execute("SELECT * FROM Projects WHERE project_ID=?", x)
		info = c.fetchone()
		#print(info)
		table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4]))

	#Create field to view/manage a certain project
	select_label = Label(root, text="Project ID Number:")
	select_label.grid(row=3, column=0, sticky=E)
	proj_select_box = Entry(root, width=30)
	proj_select_box.grid(row=3, column=1)

	view_proj_btn = Button(root, text="View Project", command=lambda: projectPage.View_Project(proj_select_box.get()))
	view_proj_btn.grid(row=4, column=0, columnspan=2)
	manage_proj_btn = Button(root, text="Manage Project", command=lambda: Manage_Project(proj_select_box.get()))
	manage_proj_btn.grid(row=5, column=0, columnspan=2)


	#Place "Create New Project" button
	create_proj_btn = Button(root, text="Create New Project", command=Create_Project)
	create_proj_btn.grid(row=6, column=0, columnspan=2)


	#Close connection
	conn.close()


#Enter event loop
root.mainloop()