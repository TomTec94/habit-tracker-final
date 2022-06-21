from db import get_habits, get_check, time_stamp_check, get_habits_with_same_per, get_tracker


def show_habits(db):
    """
    :param db: used db
    :return: Count of the rows/habits in the db table habits
    """
    data = get_habits(db)
    print(data)
    return len(data)


def show_tracker(db):
    """
    :param db: used db
    :return: shows all the habits and their current streak
    """
    data = get_tracker(db)
    return data


def calculate_check(db, name):
    """
    :param db: used db
    :param name: name of the habit
    :return: how many checks for the given habit
    """
    data = get_check(db, name)
    return len(data)


def show_checks(db, name):
    """

    :param db:
    :param name: name of the habit
    :return: shows the time stamps of the checks
    """
    data = time_stamp_check(db, name)
    return data


def same_per(db, periodicity):
    """
    :param db:
    :param periodicity: daily or weekly
    :return: shows all habits with the same periodicity
    """
    data = get_habits_with_same_per(db, periodicity)
    return data




