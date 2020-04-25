from tkinter import *
import sqlite3
import datetime as dt

#for connecting files, we can put everything below this in a function then have a button on the homepage call that function

root = Tk()
root.title("Bug Tracker")
root.geometry("600x600")

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
        project_ID Integer REFERENCES Projects )
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
        date_created Text )
        """)
except(sqlite3.OperationalError):
    print("Table \'Projects\' already exists")


def projMan():
	return

def tickMan():
	return



'''def character_limit(entry_text):
    value = dayValue.get()
    if len(value) > 2:
    	dayValue.set(value[:2])'''

#entry_text = StringVar()
#dayValue.trace('w', limitSizeDay)
ticketCounter = 0
def submitTicket():
	global ticketCounter
	#conenct to conn
	conn = sqlite3.connect('info.db')
	#create cursor
	c = conn.cursor()

	ticketStatus = "In Progress"
	date = str(dt.date.today())
	projID = 1
	#insert into table
	c.execute("INSERT INTO Tickets VALUES (:ticket_ID, :title, :description, :ticket_type, :priority, :status, :date_created, :project_ID)",
		{
			'ticket_ID' : ticketCounter,
			'title' : enterTicketName.get(),
			'description' : enterTicketDescription.get(),
			'ticket_type' : str(clicked1),
			'priority' : str(clicked2),
			'status' : ticketStatus,
			'date_created': date,
			'project_ID': projID
		}
		)
		
	ticketCounter = ticketCounter + 1

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

	'''global name_entry
	name_entry = StringVar()
	name_entry.trace('w', )'''

	newTicketName = Label(editor, text="Title (required)")
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
	enterTicketDescription.grid(row=3, column=0, padx=15, pady=(0,10))

	global clicked1
	clicked1 = StringVar()
	clicked1.set("Bug")
	global clicked2
	clicked2 = StringVar()
	clicked2.set("Minor")

	
	pickType = OptionMenu(editor, clicked1, "Bug", "Feature")
	pickType.grid(row=5, column=0, pady=(0,10))
	pickPriority = OptionMenu(editor, clicked2, "Critical", "Major", "Minor", "Trivial")
	pickPriority.grid(row=7, column=0, pady=(0,10))

	submitBtn = Button(editor, text="Create ticket", command=submitTicket)
	submitBtn.grid(row=8, column=0, pady=(10,0))

	#Commit changes
	conn.commit()
	#Close connection
	conn.close()

	editor.mainloop()

#update the list of tickets
def query():
	#conenct to conn
	conn = sqlite3.connect('info.db')
	#create cursor
	c = conn.cursor()

	#query the database
	c.execute("SELECT * FROM Tickets")
	records = c.fetchall()
	#print(records)
	#fetchall gets all records
	#fetchone gets the top record
	#fetchmany lets you designate how many

	print_records = ''
	for record in records:
		print_records += str(record) + "\n"

	query_label = Label(root, text=print_records)
	query_label.grid(row=12, column=0, columnspan=2)

	#commit changes to conn
	conn.commit()
	#close conn
	conn.close()

#make labels
projName = Label(root, text="name placeholder")
projName.config(font=("", 16))
projName.grid(row=0, column=0, columnspan=2, padx=(45,100), pady=(10,0))
projDescription = Label(root, text="description placeholder")
projDescription.config(font=("", 12))
projDescription.grid(row=2, column=0, padx=(20,0))
ticketTitle = Label(root, text="Tickets")
ticketTitle.config(font=("", 16))
ticketTitle.grid(row=3, column=0, pady=(15,0), padx=(25,0))

#make buttons
manageProj = Button(root, text="Manage Project", command=projMan)
manageProj.grid(row=0, column=2, pady=(10,0))
manageTicket = Button(root, text="Manage Ticket", command=tickMan)
manageTicket.grid(row=1, column=2)
createTicket = Button(root, text="Create Ticket", command=tickNew)
createTicket.grid(row=5, column=1, pady=(10,0))
showTickets = Button(root, text="Show Tickets", command=query)
showTickets.grid(row=3, column=2, pady=(10,0))



#Commit changes
conn.commit()
#Close connection
conn.close()


#Enter event loop 
root.mainloop()
