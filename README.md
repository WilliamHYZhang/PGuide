# PGuide Description
A web application that allows users to view and provide feedback on specific psets for their classes.

# Background
Harvard currently has a QGuide, which allows students to view and provide feedback for courses that they have taken. However, no such resource exists for PSETs. Students might want to know which PSETs will be harder and take longer to plan out their weeks. It may be helpful to read feedback from other students, like if TFs were helpful. All of this can be accomplished with a PGuide, or a QGuide for PSETs.

Anyone will be able to view feedback for PSETs for classes. Users must log in to give feedback. Admins can create the classes and the PSETs that users will use.

# Installation
Execute cd in VS Code.

Next execute
wget ...
in order to download a ZIP called pguide.zip into VS Code.

Then execute
unzip pguide.zip
to create a folder called pguide. 

You no longer need the ZIP file, so you can execute
rm pguide.zip
and respond with “y” followed by Enter at the prompt to remove the ZIP file you downloaded.

Now type
cd pguide
followed by Enter to move yourself into (i.e., open) that directory. Your prompt should now resemble the below.

pguide/ $
Execute ls by itself, and you should see a few files and folders:

app.py  DESIGN.md  helpers.py  README.md pguide.db requirements.txt  schema.sql static/  templates/

Also, install the required programs by running
pip install -r requirements.txt

We use `sqlite3` for our backend database.

# Usage

To view the website, run
flask run

# For all users

# Homepage
When a user opens PGuide, the user should be able to view a table that lists the classes that have been added by the admin. The table has columns for class name and class code.

Clicking on the class code will take the user to a class page with feedback for the psets in that class and the option to add feedback for specific psets.

The PGuide logo is on the top left. Clicking on the logo will cause the home page to reload.

On the top right, there is a navigation bar that includes "register" and "log in."

If the user is already logged in, the navigation bar will only have "log out."

# Registration Page
Clicking on register on the homepage will take you to a register page that asks for a username, password, and confirmation of your password. All fields are required, usernames must be unique, and the password and password confirmation must match.

After registration, the user will be returned to the home page.

# Login Page
Clicking on log in on the homepage will take you to a log in page that asks for a valid username and the corresponding password.

After logging in, the user will be returned to the home page.

# Class Page
Clicking on a class code on the homepage will take you to the class' page. The page will display the statistics (average overall rating, average difficulty rating, average enjoyment, distribution of hours spent, and comments) for every PSET based on feedback from users. This page also displays the overview statistics for the class, showing graphs of a comparison of overall rating, difficulty, enjoyment, and hours spent across different PSETs. Users have the option to download graphs, zoom in/out, pan, select, autoscale and reset axis.

At the bottom of the page, there is an add feedback button that will prompt a dropdown selection of all of the PSETs. If the user is not logged in, choosing a PSET to add feedback to will direct them to the log in page. If the user is logged in, hoosing a PSET to add feedback to will direct them to the feedback page.

# Feedback Page
Clicking on add feedback on the class page, while looged in, will take you to the feedback page. This page displays a form that asks for overall rating, difficulty, enjoyment, hours spent, and comments. Sliders that increment by 1 on a scale of 1-10 are used from overall rating, difficulty, and enjoyment. The value of the slider is displayed on the right of the slider so the user will know what value they are submitting. Hours spent has an input box to type a number or buttons that allow the user to increment to the number they want to submit. Comments is an input box that takes in anything. If not all fields are completed (with the exception of comments, which are optional), there will be an error. If rating, difficulty, enjoyment, and hours spent are not integer values, there will be an error.

Clicking add feedback will submit the feedback and redirect the user to the class page, where the statistics will be updated with the new feedback.

If a user submits another feedback for a PSET that they have already submitted feedback for, the new feedback will replace the previous feedback.

# For admin
Log in for admin access on the log in page, which can be reached from the navigation bar on the homepage.
Use this log in:
Username: admin
Password: pguide

# Homepage
When an admin logs in to PGuide and is redirected to the homepage, the user should be able to view a table that lists the classes. The table has columns for class name and class code, like for all users, but there will also be an edit column. Each class has an edit button under the edit column.

At the bottom of the page, there is also an add class button.

Clicking on the class code will take the admin to a class page with feedback for the psets in that class and the option to add feedback for specific psets, like all users.

Clicking on the edit button will take the admin to an edit page which allows admin to change the # of PSETs by adding or deleting PSETs and change the name and description for existing PSETs.

Clicking on the add class button will take the admin to a create page which allows admin to create new classes for all users to use and see.

The PGuide logo is on the top left. Clicking on the logo will cause the home page to reload.

On the top right, there is a navigation bar that allows the admin to "log out."

# Create Page
Clicking on the add class button on the homepage will take the admin to the create page. The create page asks for the class code, class name, and # of PSETs.

Once the admin clicks the create class button after filling out class code, class name, and # of PSETs, new items will appear on the page. Based on the # of PSETs submitted, there will be questions for each PSET that ask for the PSET name and description. After all of PSET names and descriptions are filled in, there is a submit button.

Clicking on the submit button at the bottom of the page will redirect the admin to the homepage.

# Edit Page
Clicking on one of the edit buttons on the homepage will take the admin to the edit page for the specific class that is being edited. The edit page displays a table with columns for pset name, pset description, and changes. For each pset for the class, the name, description, and options to update or delete the pset is available on the table. At the bottom of the page, there are input boxes for a new PSET name and a new PSET description, with a button to add PSET.

Clicking on the update button for a specific PSET will cause a new row of items to appear on the page. There will be an input box for an updated PSET name under the PSET name column, an input box for an updated PSET description under the PSET description box, and a confirm button under the changes column. Clicking the confirm button will update the PSET name and refresh the edit page with the changes.

Clicking on the delete button for a specific PSET will refresh the edit page and delete the PSET.

Clicking on the add PSET button on the bottom of the page after filling out the new PSET name and description input boxes will refresh the edit page with the new PSET added to the table.

# Class Page
Same as for all users.

# Feedback Page
Same as for all users.