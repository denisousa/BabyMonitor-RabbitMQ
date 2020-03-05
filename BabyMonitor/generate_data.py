from sqlalchemy.sql import select
import random
import model_baby_monitor

crying = False
sleeping = True
breathing = True
time_no_breathing = 0

def data_from_baby(count):
    global crying, sleeping, breathing, time_no_breathing

    if count == 0:
        crying = random.choices([True, False], [0.25,0.75], k=1)[0]

    if crying:
        sleeping = False
        breathing = True
        time_no_breathing = 0 
    
    else: 
        sleeping = random.choices([True, False], [0.75, 0.25], k = 1)[0]
        breathing = random.choices([True, False], [0.75, 0.25], k = 1)[0]

        if not breathing: 
            time_no_breathing += 1
        
        else: 
            time_no_breathing = 0
    
    return {'breathing': breathing, 'time_no_breathing': time_no_breathing, 'crying': crying, 'sleeping': sleeping}

