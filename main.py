import questionary
from db import get_db, get_habits, get_periodicity, check_habit_break, check_new_record, delete_habit, habit_already_existing_check, get_habits_complete
from habit import Habit
from analytic import show_habits, calculate_check, show_checks, same_per
from datetime import date


def cli():
    db = get_db()
    #test_habit(db)
    #insert_testing_data(db)

    stop = False
    while not stop:
        #main user menu with the 4 possible choices
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Check", "Analyze", "Delete", "Exit"]).ask()

        # User want to create a new habit
        if choice == "Create":
            # determine a name
            name = questionary.text("What's the name of your habit?").ask()
            # chose the periodicity the user want to check for the habit
            per = questionary.select(
                "What's the periodicity of your habit?",
                choices=["Daily", "Weekly"]).ask()
            if per == "Daily":
                per = 1
            else:
                per = 7
            if habit_already_existing_check(db, name):
                print("Habit already exists")
            else:
                habit = Habit(name, per)
                habit.store(db)
        # User want to mark a habit as done
        elif choice == "Check":
            name = questionary.text("What's the name of the habit you want to check?").ask()
            # get the habit via the name
            event_date = questionary.select("For which date do you want to check the habit (YYYY-MM-DD)?",
                                            choices=["Today", "Another day"]).ask()
            if event_date == "Today":
                event_date = str(date.today())
            else:
                event_date = questionary.text("YYYY-MM-DD").ask()
            habit = Habit(name, get_periodicity(db, name))
            # check if the habit was already checked the same day
            result = habit.add_event(db, name, event_date)
            if not result:
                pass
            habit.check_habit(db, name)
            # check if the habit streak is running or broken
            check_habit_break(db, name)
            check_new_record(db, name)

        # User want to analyze the habit/s
        elif choice == "Analyze":
            analyze_choice = questionary.select(
                "What do you want to analyze?",
                choices=["Habits", "Count of Checks", "Date and Time of Checks of a Habit",
                         "Habits with the same Periodicity", "Habit(s) with the longest streak",
                         "Longest run streak for a chosen habit"]).ask()
            # see the the history of checks for a chosen habit
            if analyze_choice == "Count of Checks":
                name = questionary.text("What's the name of your habit?").ask()
                checks = calculate_check(db, name)
                print(f" There are {checks} checks for {name}")
            # see all the habits the user entered
            elif analyze_choice == "Habits":
                count = show_habits(db)
                print(f" There are {count} habits")
            # see when a specific habit got checked
            elif analyze_choice == "Date and Time of Checks of a Habit":
                name = questionary.text("What's the name of your habit?").ask()
                time_stamps = show_checks(db, name)
                print(f"The Habit {name} has been checked on the following times {time_stamps}")
            # retrieve Habits with daily or weekly periodicity
            elif analyze_choice == "Habits with the same Periodicity":
                per = questionary.select(
                    "What's the periodicity?",
                    choices=["Daily", "Weekly"]).ask()
                if per == "Daily":
                    per = 1
                else:
                    per = 7
                which_per = same_per(db, per)
                print(f" The Habits with the periodicity of {per} are {which_per}")
            # whats are the current longest streak
            elif analyze_choice == "Habit(s) with the longest streak":
                habits = get_habits_complete(db)
                longest_streak = 0
                longest_streak_habit = ""
                # go through all habits and looking for the greatest longest_streak entry
                for habit in habits:
                    if habit[4] > longest_streak:
                        longest_streak = habit[4]
                        longest_streak_habit = habit[0]
                print(f" The habit with the longest streak is {longest_streak_habit} with {longest_streak} checks")
            elif analyze_choice == "Longest run streak for a chosen habit":
                name = questionary.text("What's the name of your habit?").ask()
                habits = get_habits_complete(db)
                for habit in habits:
                    if habit[0] == name:
                        print(f" The habit {name} has the longest streak of {habit[4]} checks")
                        print(f" and a current streak of {habit[3]} checks")
                        break
        # delete a habit with the chosen name
        elif choice == "Delete":
            name = questionary.text("What's the name of the habit you want to delete?").ask()
            delete_habit(db, name)
        else:
            print("Bye")
            stop = True


if __name__ == '__main__':
    cli()
