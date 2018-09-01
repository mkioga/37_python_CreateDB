

# ============================================
# How to check which databases are being used
# ============================================
# When you run this code, it gives you this result, which shows all the databases being used.
# Hence you can use this information to do SQL injection attack.

# ('table', 'contacts1', 'contacts1', 2, 'CREATE TABLE contacts1 (name TEXT, phone INTEGER, email TEXT)')
# ('table', 'contacts3', 'contacts3', 3, 'CREATE TABLE contacts3 (name TEXT, phone INTEGER, email TEXT)')



import sqlite3

conn = sqlite3.connect("contacts3.sqlite")

for row in conn.execute("SELECT * FROM sqlite_master"):
    print(row)

conn.close()


# ===============================================
# CHALLENGE
# ===============================================

# Modify the checkdb program to ask the user to enter a name, then use a WHERE clause in the SQL statement
# to retrieve just the row for that one person
# Check section 7 on tuples for ideas
# Before you start, remember to change the name back to "contacts3" from sqlite.master


# ========================
# MY SOLUTION
# ========================


import sqlite3

conn = sqlite3.connect("contacts3.sqlite")

name1 = input("Please enter a name: ")

for name, phone, email in conn.execute("SELECT * FROM contacts3"):
    print("{}: {}: {}".format(name, phone, email))

print("="*40)

for name, phone, email in conn.execute("SELECT * FROM contacts3"):
    if name == name1:
        print("{}: {}: {}".format(name, phone, email))
        print("-"*20)


conn.close()




# =========================================
# TRAINERS SOLUTION USING PLACEHOLDER (?):
# =========================================


import sqlite3

conn = sqlite3.connect("contacts3.sqlite")

name1 = input("Please enter a name: ")

for name, phone, email in conn.execute("SELECT * FROM contacts3"):
    print("{}: {}: {}".format(name, phone, email))

print("="*40)

# We are using placeholder (?) and assign it one tuple (name1)
# NOTE that since we are only assigning tuple with one value, it ends in a , (name1,)
# Remember its not the parenthesis that defines a tuple, its the fact that more than one value is passed.
# so if you are passing only one value, you need a comma at the end

# NOTE that = is case sensitive, so if you type "dylan" instead of "Dylan", you get no results
# To get rid of case sensitivity, use LIKE instead of =

# NOTE: if you put name1 without parenthesis in this code, and type Dylan, you get error
# "The current statement uses 1, and there are 5 supplied."
# Same thing happens if you forget the comma and type (name1) instead of (name1,)
# This is just counting the number of characters in "Dylan" which is 5 and not the number of parameters given
# If you get weird errors, paste the whole error line in google to find solution


for row in conn.execute("SELECT * FROM contacts3 WHERE name = ?", (name1,)):
    print(row)

conn.close()


