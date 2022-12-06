# Mapping tables

We began by mapping out the tables that we would need:

The users table includes id, username, password hash, and is_admin. The usernames must be unique to avoid multiple users operating under the same username. Additionally, we decided to create a column for is_admin to store a boolean (true if user has admin access, false if not) instead of creating an entirely new table for admins for concision.

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

# app.py

# styles.css

# javascript