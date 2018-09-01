
# ========================================================
# SQL Injection Attacks
# ========================================================

# (1) We will create a new contacts3.sqlite table and populate it with data below
# (2) Then we have another code to update the table

# ====================================
# (1) Code to create contacts3.sqlite
# ====================================

# Here we are using cursor objects to execute SQL queries against our database

import sqlite3

db = sqlite3.connect("contacts3.sqlite")
db.execute("DROP table contacts3")  # This will drop table so we can recreate it for our experiments
db.execute("CREATE TABLE IF NOT EXISTS contacts3 (name TEXT, phone INTEGER, email TEXT)")

db.execute("INSERT INTO contacts3 (name, phone, email) VALUES('Tim', 2222, 'tim@email.com')")
db.execute("INSERT INTO contacts3(name, phone, email) VALUES ('Dylan', 5555, 'dylan@gmail.com')")
db.execute("INSERT INTO contacts3 VALUES ('Maren', 7777, 'maren@email.com')")

cursor = db.cursor()
cursor.execute("SELECT * FROM contacts3")

# This "FETCHALL" returns a list containing a tuple for each row in the database.

print(cursor.fetchall())

for name, phone, email in cursor:
    print(name)
    print(phone)
    print(email)
    print("-" * 20)

# The "FETCHONE" method returns one row at a time
# If there is nothing in that row, it returns "None" e.g. row 4

print("=" *20)
cursor.execute("SELECT * FROM contacts3")
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())

# then we close the cursor and close database

cursor.close()

db.commit()  # commits the data to database contacts3.sqlite

db.close()


# ==========================================
# (2) Code to update table contacts3.sqlite
# ==========================================

# Now we want to update phone for Maren to 999999999

import sqlite3

db = sqlite3.connect("contacts3.sqlite")

# Now we print the results before Phone is updated

print("="*40)
print("Results Before Maren's Phone updated:")
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# update_phone is given code to update contacts3 phone where name is Maren
update_phone = "UPDATE contacts3 SET phone = 999999999 WHERE name = 'Maren'"

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

# We can check if our "db = sqlite3.connect("contacts3.sqlite")" is the same as "update_cursor.connection"
# They should be same in this case and the answer will be true.

print("="*40)
print("Are customer connections the same = {}".format(update_cursor.connection == db))


# Then we close update_cursor
update_cursor.close()

# Now we print the updated Rows

print("="*40)
print("Results after Maren's Phone updated:")
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# NOTE that we can even unpack the tuple returned above.

db.close()



# ===================================================
# SQL Injection Attack
# ===================================================

# In above code to update Maren's phone, we hard coded the new phone 9999999999 and the condition (Maren) in the statement
# Normally you want to provide these details from Variables so users can determine what to change.
# So we will create variables to store the Name and new Phone number; See CHANGE_1

import sqlite3

db = sqlite3.connect("contacts3.sqlite")

# Now we print the results before Phone is updated

print("="*40)
print("Original Names:")
print("="*40)
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# CHANGE_1

# We can define the new_phone and Name here:

# new_phone = 8888888888
# name = 'Maren'

# Or we can have user input the new_ame and phone

phone = input("Please enter Phone: ")
new_name = input("Please Enter New Name: ")


# CHANGE_1
# Then we update the update_phone string with placeholders {} to get new artuments
# NOTE for name, you need to include placeholder {} in quotes

# NOTE that when using "update_cursor.execute" command, python will not allow multiple statements to be executed.
# For example if you input two names e.g. Dylan; Maren, the code will not update anything
# Also if you add two phone numbers e.g. 777777; 999999, it will give error saying execute does not allow multiple statements

# Sometimes we want to execute multiple statements and we use EXECUTESCRIPT statement
# "executescript" is designed to run more than one SQL statement in a single call separated by semicolon
# NOTE: When I enter two names for the search i.e. WHERE name = Maren;Dylan, program runs but does not update
# But when I set two phones, say 88888;9999, it gives syntax error

# =====================
# SQL Injection Attack
# =====================
# And when I search by "Maren;DROP TABLE contacts3" This is supposed to give an error because it deletes table contacts3
# In my case, there is no update. Maybe there was a fix
# But this is supposed to be the SQL injection attack where you input bad commands to do bad things to SQL table

# When I changed to search by integer phone, I was able to set two parameters "7777; drop table contacts3"
# And it deleted the table contacts3 hence giving the error "no such table: contacts3

# This is what is called a SQL injection attack, where an attacker injects SQL statements into the SQL that a program executes
# The attacker can make some queries to find out which database is being used (contacts3 in this case)
# This query can be done like shown in checkdb.py file

# NOTE: if you use execute instead of executescript, it will not run and will give warning that you can
# only execute one statement at a time

update_name = "UPDATE contacts3 SET name = '{}' WHERE phone = {}".format(new_name, phone)
print(update_name)  # This prints above SQL statement that is sent to the database
update_cursor = db.cursor()
# update_cursor.execute(update_phone)      # This executes only one statement
update_cursor.executescript(update_name)  # This executes multiple statements

# Now we count the rows that have been updated and then print it
print("="*40)
rows_updated = update_cursor.rowcount
print("Rows Updated = {}".format(rows_updated))

# "commit" changes
update_cursor.connection.commit()

# Then we close update_cursor
update_cursor.close()

# Now we print the updated Rows

print("="*40)
print("New Names:")
print("="*40)
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# NOTE that we can even unpack the tuple returned above.

db.close()




# ================================================================
# PLACEHOLDERS and PARAMETER substitution to prevent attacks
# ================================================================

# CHANGE_1: For placeholders, we will use ? in place of {}
# CHANGE_2: ADD (new_name, phone) to original update_cursor.execute(update_name)

# When you run this code, it works, and when you try to make a SQL injection attack e.g. 7777; drop table contacts3
# Nothing happens and it shows 0 rows updated

# So using placeholders (?) (CHANGE_1), and parameter substitution (CHANGE_2) allows SQLite library to sanitize the input
# That means it will check for things like additional SQL statements that an attacker has tried to execute.


import sqlite3

db = sqlite3.connect("contacts3.sqlite")

# Now we print the results before Phone is updated

print("="*40)
print("Original Names:")
print("="*40)
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# Or we can have user input the new_ame and phone

phone = input("Please enter Phone: ")
new_name = input("Please Enter New Name: ")

# CHANGE_1
# Now we use placeholders (?)
# instead of using replacement fields {}, we use ? to indicate the places the values will be placed
# Then in our execute method (under CHANGE_2), we provide a tuple (new_name, phone) of the methods that will be used.
# The tuple should have one value for each ? in the string, in this case we have two
# We need to use parenthesis around the tuple (new_name, phone), otherwise python will interpret it as a method call with three arguments

# Note that we have not enclosed the first ? in single quotes like we did in '{}' to take a string
# This is because the library's parameter substitution takes care of correctly quoting strings where necessary



# update_name = "UPDATE contacts3 SET name = '{}' WHERE phone = {}".format(new_name, phone)  # old code using replacement fields
update_name = "UPDATE contacts3 SET name = ? WHERE phone = ?"   # using placeholders

print(update_name)  # This prints above SQL statement that is sent to the database
update_cursor = db.cursor()

# CHANGE_2: ADD (new_name, phone)

update_cursor.execute(update_name, (new_name, phone))  # CHANGE_2: ADD (new_name, phone)


# Now we count the rows that have been updated and then print it
print("="*40)
rows_updated = update_cursor.rowcount
print("Rows Updated = {}".format(rows_updated))

# "commit" changes
update_cursor.connection.commit()

# Then we close update_cursor
update_cursor.close()

# Now we print the updated Rows

print("="*40)
print("New Names:")
print("="*40)
for row in db.execute("SELECT * FROM contacts3"):
    print(row)

# NOTE that we can even unpack the tuple returned above.

db.close()

