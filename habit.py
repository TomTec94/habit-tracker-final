from datetime import datetime
from db import add_habit, check_habit_break, increment_counter, update_current_streak, check_new_record


class Habit:

    def __init__(self, name: str, periodicity: int):
        """

        :param name: user entry
        :param periodicity: user choice between 1 or 7
        """
        self.name = name
        self.periodicity = periodicity
        self.current_streak = 0
        self.longest_streak = 0

# check habit as done
    def check_habit(self, db, name):
        update_current_streak(db, name)


# store habit in the DB
    def store(self, db):
        add_habit(db, self.name, self.periodicity)


# add new event in the tracker DB-table
    def add_event(self, db, name, event_date: str = None):
        return increment_counter(db, name, event_date)