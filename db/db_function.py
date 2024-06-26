# connect_db.py

import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    database = r".\db\gymappsql.db"

    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)    

def createDB():
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id integer PRIMARY KEY AUTOINCREMENT,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        personal_id integer NOT NULL,
                                        group_id integer,
                                        card_id integer,
                                        image text
                                    ); """

    sql_create_groups_table = """CREATE TABLE IF NOT EXISTS groups (
                                    group_id integer PRIMARY KEY AUTOINCREMENT,
                                    group_name text NOT NULL,
                                    start_time datetime NOT NULL,
                                    end_time datetime NOT NULL,

                                    CONSTRAINT fk_users
                                        FOREIGN KEY (group_id)
                                        REFERENCES users (user_id)
                                        ON DELETE CASCADE
                                );"""
    
    sql_create_reports_table = """CREATE TABLE IF NOT EXISTS reports (
                                    report_id integer PRIMARY KEY AUTOINCREMENT,
                                    reading_date datetime NOT NULL,
                                    user_id integer,
                                    
                                    CONSTRAINT fk_users
                                        FOREIGN KEY (report_id)
                                        REFERENCES users (user_id)
                                        ON DELETE CASCADE
                                );"""
    
    sql_create_memberships_table = """CREATE TABLE IF NOT EXISTS memberships (
                                    membership_id integer PRIMARY KEY AUTOINCREMENT,
                                    pay_date datetime NOT NULL,
                                    number_of_months integer NOT NULL,
                                    user_id integer,
                                    amount integer,
                                    
                                    CONSTRAINT fk_users
                                        FOREIGN KEY (membership_id)
                                        REFERENCES users (user_id)
                                        ON DELETE CASCADE
                                );"""
    
    sql_create_chips_table = """CREATE TABLE IF NOT EXISTS chips (
                                    chip_id integer PRIMARY KEY,
                                    insert_date datetime NOT NULL,
                                    user_id integer,
                                    
                                    CONSTRAINT fk_users
                                        FOREIGN KEY (chip_id)
                                        REFERENCES users (user_id)
                                        ON DELETE CASCADE
                                );"""
    
    sql_create_administrators_table = """CREATE TABLE IF NOT EXISTS administrators (
                                    username text PRIMARY KEY,
                                    password text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        create_table(conn, sql_create_users_table)

        create_table(conn, sql_create_groups_table)

        create_table(conn, sql_create_reports_table)

        create_table(conn, sql_create_memberships_table)

        create_table(conn, sql_create_chips_table)

        create_table(conn, sql_create_administrators_table)
    else:
        print("Error! Cannot create the database connection.")

    conn.commit()
    conn.close()   

def insertUser(newUser):
    query = """ INSERT INTO users VALUES (null, :first_name, :last_name, :personal_id, :part_of_group, :card_id, :image) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newUser)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close
            return cursor.lastrowid

def updateUser(newUser):
    query = """ UPDATE users SET first_name = ?, last_name = ?, personal_id = ?, group_id = ?, card_id = ?, image = ? WHERE user_id = ? """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newUser)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getUsers():
    query = """ SELECT * FROM users """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def searchUsers(searchText):
    query = """ SELECT * FROM users WHERE first_name LIKE ? or last_name LIKE ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (searchText + "%", searchText + "%",))
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def deleteUser(id):
    query = """ DELETE FROM users WHERE user_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getUsersWithGroupsName():
    query = """ SELECT * FROM users LEFT JOIN groups USING (group_id); """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def insertGroup(newGroup):
    query = """ INSERT INTO groups VALUES (null, :group_name, :start_time, :end_time) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newGroup)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def updateGroup(newGroup):
    query = """ UPDATE groups SET group_name = ?, start_time = ?, end_time = ? WHERE group_id = ? """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newGroup)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getGroups():
    query = """ SELECT * FROM groups """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getGroupById(id):
    query = """ SELECT * FROM groups WHERE group_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def deleteGroup(id):
    query = """ DELETE FROM groups WHERE group_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close
            
def insertMembership(newMembership):
    query = """ INSERT INTO memberships VALUES (null, :pay_date, :number_of_months, :user_id, :amount) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newMembership)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def updateMembership(newMembership):
    query = """ UPDATE memberships SET pay_date = ?, number_of_months = ?, amount = ? WHERE membership_id = ? """
    
    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newMembership)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getMembershipByUserId(id):
    query = """ SELECT * FROM memberships WHERE user_id = ? ORDER BY pay_date DESC """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getLastPayDateMembershipByUserId(id):
    query = """ SELECT * FROM memberships WHERE user_id = ? ORDER BY pay_date DESC LIMIT 1 """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getMembershipsWithUser():
    query = """ SELECT * FROM memberships LEFT JOIN users USING (user_id); """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getMembershipsByChipId(chipId):
    query = """ SELECT * FROM memberships LEFT JOIN users USING (user_id) WHERE card_id = ? ORDER BY pay_date DESC LIMIT 1 ; """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (chipId,))
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def deleteMembership(id):
    query = """ DELETE FROM memberships WHERE membership_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def deleteMembershipByUserId(id):
    query = """ DELETE FROM memberships WHERE user_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def insertChip(newChip):
    query = """ INSERT INTO chips VALUES (:chip_id, :insert_date, :user_id) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newChip)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def updateChip(newChip):
    query = """ UPDATE chips SET insert_date = ?, user_id = ? WHERE chip_id = ? """
    
    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newChip)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getEmptyChips():
    print("get chips")

    query = """ SELECT * FROM chips WHERE user_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (-1, ))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getChipsWithUsers():
    query = """ SELECT * FROM chips LEFT JOIN users USING (user_id); """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def deleteChip(id):
    query = """ DELETE FROM chips WHERE chip_id = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def insertAdministrator(newAdministrator):
    query = """ INSERT INTO administrators VALUES (:username, :password) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newAdministrator)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def updateAdministrator(newAdministrator):
    query = """ UPDATE administrators SET password = ? WHERE username = ? """
    
    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newAdministrator)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getAdministartor():
    query = """ SELECT * FROM administrators """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getAdministartorByUsername(username):
    query = """ SELECT * FROM administrators WHERE username = ? """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def insertReport(newReport):
    query = """ INSERT INTO reports VALUES (null, :reading_date, :user_id) """

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, newReport)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getReports():
    query = """ SELECT * FROM reports """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close

def getReportsWithUsers():
    query = """ SELECT * FROM reports LEFT JOIN users USING (user_id); """

    # create a database connection
    conn = create_connection()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close