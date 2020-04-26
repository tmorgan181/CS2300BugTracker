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

    #Get the current date
    curr_date = datetime.now()
    curr_date.isoformat()
    #Only keep YYYY-MM-DD
    curr_date = str(curr_date)[:10]

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
            'date_created': curr_date,
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

#update the list of tickets
def query(project_window, proj_ID):
    #conenct to conn
    conn = sqlite3.connect('info.db')
    #create cursor
    c = conn.cursor()

    #query the database
    c.execute("SELECT * FROM Tickets WHERE project_ID=?", proj_ID)
    records = c.fetchall()
    #print(records)
    #fetchall gets all records
    #fetchone gets the top record
    #fetchmany lets you designate how many

    #Configure table
    table = Treeview(project_window)
    table['columns'] = ('ID_num', 'title', 'desc', 'type', 'priority', 'date_created')
    table['show'] = 'headings'
    table.heading('ID_num', text='ID #')
    table.column('ID_num', anchor='center', width=25)
    table.heading('title', text='title')
    table.column('title', anchor='center', width=100)
    table.heading('desc', text='Description')
    table.column('desc', anchor='center', width=250)
    table.heading('type', text='Ticket Type')
    table.column('type', anchor='center', width=25)
    table.heading('priority', text='Ticket Priority')
    table.column('priority', anchor='center', width=25)
    table.heading('date_created', text='Created On')
    table.column('date_created', anchor='center', width=100)
    table.grid(columnspan=3, sticky = (N,S,W,E))

    for info in records:
        print(info)
        table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[5]))

    #close conn
    conn.close()

def View_Project(proj_ID):
    #Open project window
    project_window = Toplevel()
    project_window.geometry("500x500")
    project_window.title("View Project")

    #conenct to conn
    conn = sqlite3.connect('info.db')
    #create cursor
    c = conn.cursor()

    #Fetch project data
    c.execute("SELECT * FROM Projects WHERE project_ID=?", proj_ID)
    data = c.fetchone()
    print(data)

    #make labels
    projName = Label(project_window, text=data[1])
    projName.grid(row=0, column=0, columnspan=2)
    projDescription = Label(project_window, text=data[2])
    projDescription.grid(row=1, column=0, columnspan=2)
    ticketTitle = Label(project_window, text="Tickets")
    ticketTitle.configure(font="TkDefaultFont 10 underline")
    ticketTitle.grid(row=4, column=0, columnspan=2, sticky=W)

    #make buttons
    manageTicket = Button(project_window, text="Manage Tickets", command=tickMan)
    manageTicket.grid(row=2, column=1)
    createTicket = Button(project_window, text="Create New Ticket", command=tickNew)
    createTicket.grid(row=2, column=0)

    #query the database
    c.execute("SELECT * FROM Tickets WHERE project_ID=?", proj_ID)
    records = c.fetchall()
    print(records)

    #Configure table
    table = Treeview(project_window)
    table['columns'] = ('ID_num', 'title', 'desc', 'type', 'priority', 'date_created')
    table['show'] = 'headings'
    table.heading('ID_num', text='ID #')
    table.column('ID_num', anchor='center', width=25)
    table.heading('title', text='title')
    table.column('title', anchor='center', width=100)
    table.heading('desc', text='Description')
    table.column('desc', anchor='center', width=250)
    table.heading('type', text='Ticket Type')
    table.column('type', anchor='center', width=25)
    table.heading('priority', text='Ticket Priority')
    table.column('priority', anchor='center', width=25)
    table.heading('date_created', text='Created On')
    table.column('date_created', anchor='center', width=100)
    table.grid(columnspan=3, sticky = (N,S,W,E))

    for info in records:
        print(info)
        table.insert("", "end", values=(info[0], info[1], info[2], info[3], info[4], info[5]))

    #close conn
    conn.close()

#    showTickets = Button(project_window, text="Show Tickets", command=lambda: query(project_window, proj_ID))
#    showTickets.grid(row=3, column=2, pady=(10,0))

    return