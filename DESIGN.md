# Mapping databases

We began by mapping out the databases that we would need:

The users database includes id, username, password hash, and is_admin. The usernames must be unique to avoid multiple users operating under the same username. Additionally, we decided to create a column for is_admin to store a boolean (true if user has admin access, false if not) instead of creating an entirely new database for admins for concision.

The classes database includes id, code, and name.

The psets database includes id, class_id, name, and description. class_id references id from classes to keep track of which psets are in which classes. This allows the classes and psets databases to be joined.

The feedback database includes id, user_id, pset_id, rating, hours_spent, difficulty, enjoyment, and comments. user_id references id from users to keep track of which user is submitting the feedback, allowing the users and feedback databases to be joined. This is especially useful later when we decide to update previous feedback if users resubmit feedback for the same PSET. pset_id references id from psets to keep track of which pset the feedback is being submitted to, allowing the psets and feedback databases to be joined.

See schema.sql for more information on databases

# Mapping pages

Next, we mapped out which pages we would need:

The index page serves as the homepage for 