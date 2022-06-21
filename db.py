import sqlite3

from datetime import datetime, date


# Set up a database connection
def get_db(name="main.db"):
    """

    :param name: main.db
    :return: the Database
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


# Create the needed Tables
def create_tables(db):
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS habits (
       name TEXT PRIMARY KEY,
       periodicity TEXT,
       date_created TEXT,
       current_streak INTEGER,
       longest_streak INTEGER)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        habitName TEXT,
        FOREIGN KEY (habitName) REFERENCES habits(name))""")

    db.commit()


# Add new habits
def add_habit(db, name, periodicity, date_created=None, current_streak=0, longest_streak=0):
    """

    :param db: used database
    :param name: name of the habits
    :param periodicity: wanted periodicity of the habit (1 or 7)
    :param date_created: on which date was the habit created
    :param current_streak: default 0
    :param longest_streak:  default 0
    :return:
    """
    cursor = db.cursor()
    if not date_created:
        date_created = date.today()

    cursor.execute("SELECT * FROM tracker WHERE habitName=? ", (name,))
    result = cursor.fetchall()
    if result:
        print("Habit already exists")
        db.commit()
    # else insert new habit
    else:
        cursor.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?)", (name, periodicity, date_created,
                                                                     current_streak, longest_streak))
    db.commit()


# add an entry to the tracker table, when a habit is checked
def increment_counter(db, name, event_date):
    """

    :param db: used database
    :param name: name of the habit
    :param event_date: on which day got the habit checked/the counter incremented
    :return:
    """
    cursor = db.cursor()

    # Check if the habit exists with current date
    cursor.execute("SELECT * FROM tracker WHERE habitName=? AND date=?", (name, event_date))
    result = cursor.fetchall()
    if result:
        print("Already checked today")
        db.commit()
    # else insert new event
    else:
        cursor.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name,))
        db.commit()

    return result


# retrieve all the habits (the name)
def get_habits(db):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits")
    return cursor.fetchall()


# retrieve all the habits
def get_habits_complete(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits")
    return cursor.fetchall()


# retrieve all the checked events
def get_tracker(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tracker")
    return cursor.fetchall()


def get_check(db, name):
    """

    :param db: used db
    :param name: name of the habit as key
    :return: everything from the habit with the given name
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tracker WHERE habitName=?", (name,))
    return cursor.fetchall()


def time_stamp_check(db, name):
    """

    :param db: used db
    :param name: name as key to find the habit
    :return:  date from the name of the habit
    """
    cursor = db.cursor()
    cursor.execute("SELECT date FROM tracker WHERE habitName=?", (name,))
    return cursor.fetchall()


def get_habits_with_same_per(db, periodicity):
    """

    :param db: used db
    :param periodicity: 1 or 7
    :return: all habit names with the specific periodicity
    """
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits WHERE periodicity=?", (periodicity,))
    return cursor.fetchall()


# increment current streak
def update_current_streak(db, name):
    """

    :param db: used db
    :param name: name as key to find the habit
    :return: updated DB entry
    """
    cursor = db.cursor()
    cursor.execute("UPDATE habits SET current_streak=current_streak+1 WHERE name=?", (name,))
    db.commit()


# set streak to 0
def reset_current_streak(db, name):
    """

    :param db: used db
    :param name: name as key to find the habit
    :return: update the value current streak
    """
    cursor = db.cursor()
    cursor.execute("UPDATE habits SET current_streak=1 WHERE name=?", (name,))
    db.commit()


# check is the current streak is also a new longest streak
def check_new_record(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT current_streak FROM habits WHERE name=?", (name,))
    cur_str = cursor.fetchall()
    cursor.execute("SELECT longest_streak FROM habits WHERE name=?", (name,))
    # compare current with longest streak
    long_str = cursor.fetchall()
    # update when if condition is true
    if cur_str > long_str:
        update_longest_streak(db, name)


# update value of a habit with the given name
def update_longest_streak(db, name):
    cursor = db.cursor()
    cursor.execute("UPDATE habits SET longest_streak=current_streak WHERE name=?", (name,))
    db.commit()


# decrement longest streak if a habit is broken  with the given name
def dec_longest_streak(db, name):
    cursor = db.cursor()
    cursor.execute("UPDATE habits SET longest_streak=longest_streak-1 WHERE name=?", (name,))
    db.commit()


# check is a habit was not checked during the given periodicity
def check_habit_break(db, name):
    cursor = db.cursor()
    per = get_periodicity(db, name)
    if per == 1:
        # get date from tracker if they are consecutive days then it is not broken
        cursor.execute("SELECT date FROM tracker WHERE habitName=?", (name,))
        dates = cursor.fetchall()
        # check from the newest to the 2nd newest event
        for i in reversed(range(len(dates))):
            if i == 0:
                continue
            else:
                date1 = datetime.strptime(dates[i - 1][0], '%Y-%m-%d')
                date2 = datetime.strptime(dates[i][0], '%Y-%m-%d')
                delta = date2 - date1
                if delta.days == 1:
                    break
                else:
                    print(f"Streak of the habit {name} is broken since there was not a check for 1 days")
                    reset_current_streak(db, name)
                    return False
                    break
    else:
        # get date from tracker if they are consecutive days then it is not broken
        cursor.execute("SELECT date FROM tracker WHERE habitName=?", (name,))
        dates = cursor.fetchall()
        for i in reversed(range(len(dates))):
            if i == 0:
                continue
            else:
                date1 = datetime.strptime(dates[i - 1][0], '%Y-%m-%d')
                date2 = datetime.strptime(dates[i][0], '%Y-%m-%d')
                delta = date2 - date1
                if delta.days <= 7:
                    break
                else:
                    print(f"Streak of the habit {name} is broken since there was not a check for 7 days")
                    reset_current_streak(db, name)
                    return False
                    break


# delete the specific habit from the DB-tables
def delete_habit(db, name):
    if habit_already_existing_check(db, name):
        cursor = db.cursor()
        cursor.execute("DELETE FROM tracker WHERE habitName =?", (name,))
        cursor.execute("DELETE FROM habits WHERE name =?", (name,))
        db.commit()
        print(f"The habit {name} has been deleted!")
    else:
        print(f"There is no habit {name} existing")


# return all habits with the daily or weekly periodicity
def get_periodicity(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE periodicity=7 AND name =?", (name,))
    result = cursor.fetchone()
    if result:
        per = 7
    else:
        per = 1
    return per


# check if a habit does already exists
def habit_already_existing_check(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE name=?", (name,))
    result = cursor.fetchall()
    db.commit()
    return result
    return True
