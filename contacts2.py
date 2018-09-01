
# Here we will connect to "contacts1.sqlite" and try to retrieve the data
# NOTE that you can run the code without using cursor and executiing the .connect as shown below.
# If you run this code, you get no result (before "db.commit()" was added in contacts.py.
# This is because there is no data in contacts1.sqlite because it was not committed.

import sqlite3

db = sqlite3.connect("contacts1.sqlite")

for row in db.execute("SELECT * FROM contacts1"):
    print(row)

# NOTE that we can even unpack the tuple returned above.

print("="*20)
for name, phone, email in db.execute("SELECT * FROM contacts1"):
    print(name)
    print(phone)
    print(email)
    print("-"*20)

db.close()


# NOTE: After "db.commit()" is done, we now get results here because data has been commited to database.


# ===========================================================
# UPDATING RECORDS USING CURSOR and using ROWCOUNT
# ===========================================================

# For certain updates, it makes sense to use "cursor" because cursor has a "rowcount" property to check
# how many rows have been affected by the previous SQL statement.

# The current results before phone updates are as follows:

# ('Tim', 6789654123, 'tim@email.com')
# ('Dylan', 1234567899, 'dylan@gmail.com')
# ('Maren', 4567896541, 'maren@email.com')

# Now we want to update phone for Maren to 999999999

import sqlite3

db = sqlite3.connect("contacts1.sqlite")

# Now we print the results before Phone is updated

print("="*40)
print("Results Before Maren's Phone updated:")
for row in db.execute("SELECT * FROM contacts1"):
    print(row)


# update_phone is given code to update contacts1 phone where name is Maren
update_phone = "UPDATE contacts1 SET phone = 999999999 WHERE name = 'Maren'"

# Now we define update_cursor to become db.cursor()
update_cursor = db.cursor()

# Then we execute update_cursor and pass it update_phone which has SQL code to update phone
update_cursor.execute(update_phone)

# Now we count the rows that have been updated and then print it
print("="*40)
rows_updated = update_cursor.rowcount
print("Rows Updated = {}".format(rows_updated))

# NOTE: After you test all your updates and they work as required, then you can "commit"
# the changes using "cursor.connection.commit()" so that they are stored in the database
# NOTE: It is advisable to use "cursor commit" instead of "db.commit" because in more complex programs
# you may have functions that deal with UPDATES and INSERTS and they may have a "cursor" object to do the commit
# But the function may not actually know or need to know about the program connection.

# Another reason its advisable to use cursor to commit is you may also create more than one connection to the database
# and if you do db.commit on the wrong connection, this can introduce subtle bugs that are hard to find if it gives you a commit error.
# So its better to use the cursors connection property to get a reference to the connection that the cursor is using and then call a
# commit on that.

update_cursor.connection.commit()

# We can check if our "db = sqlite3.connect("contacts1.sqlite")" is the same as "update_cursor.connection"
# They should be same in this case and the answer will be true.

print("="*40)
print("Are customer connections the same = {}".format(update_cursor.connection == db))


# Then we close update_cursor
update_cursor.close()

# Now we print the updated Rows

print("="*40)
print("Results after Maren's Phone updated:")
for row in db.execute("SELECT * FROM contacts1"):
    print(row)

# NOTE that we can even unpack the tuple returned above.

db.close()

