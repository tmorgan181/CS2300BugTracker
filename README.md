# Project Description
Created for our CS 2300 Databases class, the Bug Tracker program allows users to create and manage development projects, and associate a number of tickets with each one. Tickets detail the progress/requirements for bugs and features within the project. Our program is written in Python, using built-in Python tools for GUI (TKinter) and database (SQLite3) implementation.

# Installation/Usage
To install this program, simply clone this repository and run the Python file `Bug_Tracker.py`. This will initialize a new local database instance, where program data will be stored. As long as Python 2 or above is installed on your machine, the required dependencies will already be present.

The home page is the first screen that appears when the Bug Tracker is launched. Here, a table displays all the user's created projects and the relevant details for each. From the home page you can select a project to view, manage the project, or create a new project. Additionally, you can open a window to view all tickets within all projects. The first time the application is run, there will be no projects to populate the table display, so you must create a new one to begin using the program.

To see and manage the contents of a project, left-click to select a project, then click the “View Project” button underneath the table. This will open the project page, where the title of the project and its description are displayed at the top. Below that, a table that contains all the tickets that are contained within the project. For a newly created project, this table will be empty. From the View Project window, you can manage a project’s tickets and create new ones.

# Contributors
* [Nick Beffa](https://github.com/nbeffa)

* [Trenton Morgan](https://github.com/tmorgan181)