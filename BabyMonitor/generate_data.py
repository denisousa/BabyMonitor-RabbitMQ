from sqlalchemy.sql import select
import random

def captured_data_from_baby():
    breathing = random.choices([False, True], [0.75, 0.25], k = 1)[0]
    crying = random.choices([True, False], [0.2, 0.8], k = 1)[0]
    sleeping = True if crying else False
    time_no_breathing = 0 if breathing else 