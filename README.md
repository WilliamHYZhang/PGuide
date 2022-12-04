# PGuide Description
A web application that allows users to view and provide feedback on specific psets for their classes.

# For all users

# Homepage
When a user opens PGuide, the user should be able to view a table that lists the classes that have been added by the admin. The table has columns for class name and class code.

Clicking on the class code will take the user to a class page with feedback for the psets in that class and the option to add feedback for specific psets.

The PGuide logo is on the top left. Clicking on the logo will cause the home page to reload.

On the top right, there is a navigation bar that includes "register" and "log in."

# Registration Page
Clicking on register on the homepage will take you to a register page that asks for a username, password, and confirmation of your password. All fields are required, usernames must be unique, and the password and password confirmation must match.

After registration, the user will be returned to the home page.

# Login Page
Clicking on log in on the homepage will take you to a log in page that asks for a valid username and the corresponding password.

After logging in, the user will be returned to the home page.

# For admin

# Installation

```
pip install -r requirements.txt
```

We use `sqlite3` for our backend database.

# Usage
```
flask run
```