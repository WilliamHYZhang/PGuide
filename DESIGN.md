# Mapping tables

We began by mapping out the tables that we would need:

The users table includes id, username, password hash, and is_admin. The usernames must be unique to avoid multiple users operating under the same username. Password hashes are stored instead of passwords to maintain user privacy. Additionally, we decided to create a column for is_admin to store a boolean (true if user has admin access, false if not) instead of creating an entirely new table for admins for concision.

The classes table includes id, code, and name.

The psets table includes id, class_id, name, and description. class_id references id from classes to keep track of which psets are in which classes. This allows the classes and psets tables to be joined.

The feedback table includes id, user_id, pset_id, rating, hours_spent, difficulty, enjoyment, and comments. user_id references id from users to keep track of which user is submitting the feedback, allowing the users and feedback tables to be joined. This is especially useful later when we decide to update previous feedback if users resubmit feedback for the same PSET. pset_id references id from psets to keep track of which pset the feedback is being submitted to, allowing the psets and feedback tables to be joined.

See schema.sql for more information on tables

# Designing pages

Next, we mapped out which pages we would need and what they would look like: https://drive.google.com/file/d/1GbtMUFOt1nEDSwkHayqOeyI0KqzFmEsX/view?usp=sharing (Diagram)

On all pages, there is a navigation bar at the top. On the left, there is a PGuide logo that redirects the user to the homepage. We decided to implement this because that is what is intuitive for users. If users are on the feedback page and need an efficient way to return to the homepage, the logo can be used. On the right, there is either a registration and log in button that will take users to the respective pages or a log out button if users are already logged in. We implemented this so users are always able to register, log in, or log out. Also, if users submit forms or click buttons with errors, they are redirected to an apology page that specifies the error. 

After a user registers, they are redirected to the homepage. After a user logs in, they are redirected to the homepage. After a user logs out, they are redirected to the homepage.

The index page serves as the homepage for all users, including users with admin access, users who are logged in, and users who are not logged in. For all users, there is a table that lists the classes. However, for users with admin access, there are also options to edit existing classes or create new classes. We decided to have the homepage for all users to exist on the same file to reduce redunancy in our code. Additionally, all users can click on a class code to go to the respective class' class page, as we believed this was the most intuitive way users would understand which class page they are going to.

The class page displays overview statistics for the class. We believed this would be helpful in quickly understanding how PSETs compared with each other. Below the overview, there are statstics for each PSET. At the bottom of the page, there is an option to add feedback. Because we wanted to track which users submit what feedback, we made sure that only users who are logged in can successfully click the add feedback button and be redirected to the feedback page. If users are not logged in and they click the add feedback button, they are prompted to log in.

The feedback page allows users to input their own feedback. All fields are required to ensure that other users get a full picture of the feedback for the PSET. If a user resubmits feedback for a PSET they have already given feedback for, there previous feedback is replaced with the new feedback, which is why we wanted to track which users submit what feedback. After submitting feedback successfully, users are redirected to the class page where all statistics are updated based on the new feedback.

That concludes the capabilities of users who do not have admin access. For users who do have admin access, which can only be granted by us on the backend, there are features to edit classes.

From the homepage, admin have an option to edit classes, which will redirect them to the edit page for the specific class that is chosen to be edited. The edit page displays each PSET's name and description, so admin know what already exists and what they would want to change. The edit page also includes the option to update or delete existing PSETs or add a new PSET for the class. Clicking the update button will make 2 input boxes and a confirm button appear on the page, which allows the admin to understand what they are changing without the page being constantly cluttered. Clicking the confirm button will reload the edit page and display the table of PSET names and descriptions with the updated information. Clicking the delete button will reload the edit page and display the table of PSET names and descriptions, minus the PSET that has been deleted. Filling out the new pset name and description boxes, then clicking the add PSET button will reload the edit page and display the table of PSET name and descriptions with the new PSET. However, clicking the add PSET button with blank new pset name and description will display and error message. We chose to have the edit page reload when admin update, delete, or add PSETs so they can view the changes they make right away.

From the homepage, admin also have an option to create classes, which will redirect them to the create page. Here, admin must input the class code, name, and # of PSETs, then click the create button. If not all fields are filled out or if # of PSETs is not an integer, an error message will show. After successfully clicking the create button, PSET name and description input boxes and a submit button will appear for the amount of PSETs that the admin has selected. We chose not to direct the admin to a new page for user convenience. Once the create button has been clicked, the create button will be disabled to ensure that the admin uses the submit button to finish creating the PSETs for the class. Clicking submit after filling in the fields will successfully create the new class, update the database tables, and redirect the user to the homepage. 

# Implementation

# html templates
The login.html and register.html files used code from the finance PSET. 
We used a layout.html file, based on the finance PSET, to format items that were consistent across all pages (nav bar, logo, created by message). This helped us reduce repetitive code by using style cascading.
We used the apology.html to display an error code and error message for all user errors.

The index.html file contains a table with columns labeled with class code and class name for all users. An if statement is used to give admins access to an additional column labeled edit. In the body of the table, we use a for loop to iterate through the list of dictionaries from the classes variable in app.py, which is selected from the classes table in SQL. This will show the code and name for each class. Each class code is linked to the class page, specific to the class code. We use an if statement again to give admins access to an edit button for each class that is linked to the edit page, specific to the class code of the class that is selected to be edited. Finally, the create button at the bottom is linked to the create page.

The class.html file contains links to images that display graphs showing the statstics for the class. We chose to calculate and re-visualize the statistics everytime a user ends up on the class page, instead of storing the statistics because ... After the statistics, there is an add feedback button that turns into a dropdown menu when clicked. The dropdown will display the PSET names for the class. Each dropdown item links to the feedback page specific to the selected PSET name and its id. We chose to use this dropdown menu for user convenience and to allow users to choose which PSET to provide feedback to without cluttering the page.

The feedback.html file uses range sliders that range from 1-10, incrementing by 1 for users to provide feedback on overall rating, difficulty, and enjoyment. Javascript is used to show the users the current value of their slider for users to know exactly what feedback they are providing. Feedback for hours spent is provided by an input box that accepts numbers. This input box has arrows that allow users to increment up and down by 1 for ease of use. Comments can be provided by an input box that accepts text; however, comments are optional if users do not have more to add. The submit button is used to send the information to the backend.

The create.html file has an initial form to ask for class code, name, and # of PSETs, followed by a create button. Once the create button is clicked, new items appear asking for names and descriptions for the # of PSETs that is specified earlier. This is down using Javascript. We chose to use Javascript to display these new items because it created a flow in user usage. A submit button is in the Javascript code to submit all the information for creating PSETs while creating the class.

The edit.html file contains a table with columns labeled with PSET name, PSET description, and change. In the body of the table, we use a for loop to iterate through the list of dictionaries from the psets variable in app.py, which is selected from the psets table in SQL. This will show the name and description for each PSET. Each PSET has an update button and a delete button in the change column. The delete button is a link to the edit page where the PSET name and description for the deleted items are hidden. There is also a hidden form that asks for updated PSET name and updated PSET description with a confirm button. Using Javascript, we have an event listener for clicking the update button that will reveal the hidden form. Finally, there is another form, outside of the table, that asks for new PSET name and new PSET description, with an add PSET button to submit the form and create a new PSET.

# app.py

# helpers.py

# styles.css
We used a styles.css file to design the nav bar and the buttons we used. We chose to have a css file outside of the html because the same style is used across multiple pages, so a single, separate CSS file applies to all the pages, which is also helpful for scaleability. We also chose to use a crimson shade for our buttons and logo for Harvard!

# javascript