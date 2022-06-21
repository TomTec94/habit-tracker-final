from db import get_db, add_habit, increment_counter, get_tracker, get_habits, get_check, time_stamp_check,\
    get_habits_with_same_per,habit_already_existing_check, check_habit_break
from habit import Habit


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test1", 1, "2022-06-01", 0, 0)
        add_habit(self.db, "test2", 7, "2022-06-02", 0, 0)
        add_habit(self.db, "test3", 7, "2022-06-02", 0, 0)
        add_habit(self.db, "test4", 1, "2022-05-02", 0, 0)
        add_habit(self.db, "test5", 1, "2022-06-01", 0, 0) # Habits == 5
        increment_counter(self.db, "test1", "2022-06-02")
        increment_counter(self.db, "test1", "2022-06-03")
        increment_counter(self.db, "test1", "2022-06-04")
        increment_counter(self.db, "test1", "2022-06-05")
        increment_counter(self.db, "test1", "2022-06-06")
        increment_counter(self.db, "test2", "2022-06-05")
        increment_counter(self.db, "test2", "2022-07-06")
        increment_counter(self.db, "test3", "2022-07-06")
        increment_counter(self.db, "test3", "2022-07-12")
        increment_counter(self.db, "test3", "2022-07-15")
        increment_counter(self.db, "test3", "2022-07-30")
        increment_counter(self.db, "test4", "2022-07-06")
        increment_counter(self.db, "test5", "2022-06-10")
        increment_counter(self.db, "test5", "2022-06-11")
        increment_counter(self.db, "test5", "2022-06-12")  # Counter == 15

    def test_habit(self):
        habit1 = Habit("test-class", 7)
        print(habit1)

    def test_db_tracker(self):
        data = get_tracker(self.db)
        assert len(data) == 15

    def test_get_habits(self):
        data = get_habits(self.db)
        assert len(data) == 5

    def test_get_check(self):
        data = get_check(self.db, "test2")
        assert len(data) == 2

    def test_time_check(self):
        data = time_stamp_check(self.db, "test1")
        assert len(data) == 5

    def test_same_per(self):
        data = get_habits_with_same_per(self.db, 1)
        assert len(data) == 3

    def test_check_habit_break(self):
        data1 = check_habit_break(self.db, "test1")
        assert data1 == None
        data2 = check_habit_break(self.db, "test2")
        assert data2 == False

    def test_habit_existing(self):
        data = habit_already_existing_check(self.db, "test1")
        assert data == [('test1', '1', '2022-06-01', 0, 0)]
        data2 = habit_already_existing_check(self.db, "test99")
        assert data2 == []

    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test.db")

        



