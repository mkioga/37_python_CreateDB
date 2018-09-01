
# ===========================================================
# SQL in Python
# ===========================================================

# The python sqlite3 module that is included in python makes it easy to create SQLite databases.
# We will start by creating a "contacts" database

# first we import sqlite3 module

import sqlite3

# Then we create a connection to the database.
# we use sqlite3.connect function and call our new database "contacts.sqlite"
# NOTE we can name the database anything, but its good to prefix it with .sqlite (reason will be explained later)

db = sqlite3.connect("contacts.sqlite")

# Now we will create a TABLE by passing the SQLite statements to the connections execute function
# NOTE the "IF NOT EXISTS" is used to check if the contacts table exist and if not, it creates it again
# This avoids error where it would say "contacts table exists"

db.execute("CREATE TABLE IF NOT EXISTS contacts (name TEXT, phone INTEGER, email TEXT)")

# Now we will INSERT a line into the table.
# NOTE in third line, if you are inserting to all fields/columns in order they appear, you don't need to specify the fields.

db.execute("INSERT INTO contacts (name, phone, email) VALUES('Tim', 6789654123, 'tim@email.com')")
db.execute("INSERT INTO contacts(name, phone, email) VALUES ('Dylan', 1234567899, 'dylan@gmail.com')")
db.execute("INSERT INTO contacts VALUES ('Maren', 4567896541, 'maren@email.com')")

# We can now query the "contacts" database that we created.
# We can do this in sqlite, but can also do it here using "cursor" function
# A "cursor" is what is called a generator.
# A generator is an interval that works by generating the next value each time it is used.
# In python, you can create an interval object that count to infinity without running out of memory.
# When the code iterates over the cursor, it returns next row from the database, but does not keep track of previous rows
# So since its not a list, there is no way to go to previous records.
# That is why "TEST CODE" below does not generate any output

# NOTE: I don't see the INSERT statements when I go directly to SQLite, but results are showing up here
# NOTE that we don't use semi-colon (;) to end statements in Python for SQL

cursor = db.cursor()
cursor.execute("SELECT * FROM contacts")
for row in cursor:
    print(row)
# Above prints the rows in tuple format as shown:
# ('Tim', 6789654123, 'tim@email.com')
# ('Dylan', 1234567899, 'dylan@gmail.com')
# ('Maren', 4567896541, 'maren@email.com')

# ============================
# We can also unpack the tuple and print each of them in different line
print("=" * 20)
cursor.execute("SELECT * FROM contacts")
for name, phone, email in cursor:
    print(name)
    print(phone)
    print(email)
    print("-" * 20)
# Above will give results like this for all the records
# Tim
# 6789654123
# tim@email.com

# TEST CODE
# This for loop does not generate any output

for name, phone, email in cursor:
    print(name)
    print(phone)
    print(email)
    print("-" * 20)


# then we close the cursot
cursor.close()

# Then we close the database connection

db.close()

# Then we run the program and we see it creates a "contacts.sqlite" table at on the side.
# You can also see the table here: C:\Users\moe\Documents\Python\IdeaProjects\37_CreateDB



# ============================================
# FETCHALL and FETCHONE method
# ============================================

# Sometimes you may want the entire dataset in a single list, and instead of using "for" loop
# you can use "fetch all" method.



import sqlite3

db = sqlite3.connect("contacts1.sqlite")

db.execute("CREATE TABLE IF NOT EXISTS contacts1 (name TEXT, phone INTEGER, email TEXT)")

db.execute("INSERT INTO contacts1 (name, phone, email) VALUES('Tim', 6789654123, 'tim@email.com')")
db.execute("INSERT INTO contacts1(name, phone, email) VALUES ('Dylan', 1234567899, 'dylan@gmail.com')")
db.execute("INSERT INTO contacts1 VALUES ('Maren', 4567896541, 'maren@email.com')")

cursor = db.cursor()
cursor.execute("SELECT * FROM contacts1")

# This "FETCHALL" returns a list containing a tuple for each row in the database.

print(cursor.fetchall())

# for name, phone, email in cursor:
#     print(name)
#     print(phone)
#     print(email)
#     print("-" * 20)

# The "FETCHONE" method returns one row at a time
# If there is nothing in that row, it returns "None" e.g. row 4

print("=" *20)
cursor.execute("SELECT * FROM contacts1")
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())  # This one returns None since there are only three rows

# then we close the cursor and close database

cursor.close()

db.commit()  # Read below to understand db.commit()

db.close()

# ===================================================
# COMMIT
# ===================================================

# When you run this command in python, you get some results from the data we inserted
# But if you go to command prompt and do "SELECT * FROM contacts", you get no results
# This is because above results have not been COMMITTED to database.

# RESULTS FROM COMMAND PROMPT SHOWS NOTHING

# C:\Users\moe\Documents\Python\IdeaProjects\37_CreateDB>
# C:\Users\moe\Documents\Python\IdeaProjects\37_CreateDB>sqlite3 contacts1.sqlite
# SQLite version 3.23.1 2018-04-10 17:39:29
# Enter ".help" for usage hints.
#     sqlite>
# sqlite> .headers on
# sqlite>
# sqlite> .schema
# CREATE TABLE contacts (name TEXT, phone INTEGER, email TEXT);
# CREATE TABLE contacts1 (name TEXT, phone INTEGER, email TEXT);
# sqlite>
# sqlite>
# sqlite> .dump
# PRAGMA foreign_keys=OFF;
# BEGIN TRANSACTION;
# CREATE TABLE contacts (name TEXT, phone INTEGER, email TEXT);
# CREATE TABLE contacts1 (name TEXT, phone INTEGER, email TEXT);
# COMMIT;
# sqlite>
# sqlite>
# sqlite>
# sqlite> SELECT * FROM contacts;
# sqlite>
# sqlite> SELECT * FROM contacts1;
# sqlite>
# sqlite>
# sqlite>

# ==============================================

# Another way to check this is to create a new python file, named contacts2.py
# and connect to database "contacts1.sqlite" and then try to do SELECT * FROM contacts.
# you will get no results.

# ==============================================

# Now will add "db.commit()" above to commit data to database

# After commit is done, we can now get data from contacts1.sqlite

# sqlite>
# sqlite> SELECT * from contacts;
# sqlite>
# sqlite> SELECT * from contacts1;
# name|phone|email
# Tim|6789654123|tim@email.com
# Dylan|1234567899|dylan@gmail.com
# Maren|4567896541|maren@email.com
# sqlite>
# sqlite>
# sqlite>

# ===============================================