# PGuide Description
A web application that allows users to view and provide feedback on specific psets for their classes.

# Installation
```
pip install -r requirements.txt
```

We use `sqlite3` for our backend database.

# Usage
```
flask run
```

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
Clicking on a class code on the homepage will take you to the class' page. This page displays the overview statistics for the class, showing graphs of a comparison of overall rating, difficulty, enjoyment, and hours spent across different PSETs. The page also displays the statistics (average overall rating, average difficulty rating, average enjoyment, distribution of hours spent, and comments) for every PSET based on feedback from users.

At the bottom of the page, there is an add feedback button that will prompt a dropdown selection of all of the PSETs. If the user is not logged in, choosing a PSET to add feedback to will direct them to the log in page. If the user is logged in, hoosing a PSET to add feedback to will direct them to the feedback page.

# Feedback Page
Clicking on add feedback on the class page, while looged in, will take you to the feedback page. This page displays a form that asks for overall rating, difficulty, enjoyment, hours spent, and comments. Sliders that increment by 1 on a scale of 1-10 are used from overall rating, difficulty, and enjoyment. The value of the slider is displayed on the right of the slider so the user will know what value they are submitting. Hours spent has an input box to type a number or buttons that allow the user to increment to the number they want to submit. Comments is an input box that takes in anything. If there is not all fields are completed, there will be an error. If rating, difficulty, enjoyment, and hours spent are not integer values, there will be an error.

Clicking add feedback will submit the feedback and redirect the user to the class page, where the statistics will be updated with the new feedback.

# For admin
Log in for admin access
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