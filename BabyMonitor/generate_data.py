from sqlalchemy.sql import select
import random
from model_baby_monitor import insert_baby_monitor, get_data_baby_monitor
import sys
sys.path.append('../')
from construct_scenario import bm, engine

crying = False
sleeping = True
breathing = True
time_no_breathing = 0
max_no_changes = random.randint(5,15)


def count(function):
    
    def wrapped():
        
        global max_no_changes, breathing
        if wrapped.calls < max_no_changes:
            wrapped.calls += 1
            if wrapped.calls == 1:  
                return function(0)
            elif breathing:
                return 1 
            else: 
                return function(wrapped.calls)

        else:        
            wrapped.calls = 0 
            max_no_changes = random.randint(3,5)
            return function(0)
    
    wrapped.calls = 0
    return wrapped

@count
def data_from_baby(flag):
    global crying, sleeping, breathing, time_no_breathing

    data = {}

    if not flag:   
        crying = random.choices([True, False], [0.25,0.75], k=1)[0]

        if crying:
            sleeping = False
            breathing = True
            time_no_breathing = 0 
        
        else: 
            sleeping = random.choices([True, False], [0.75, 0.25], k = 1)[0]
            breathing = random.choices([True, False], [0.25, 0.75], k = 1)[0]

            if not breathing: 
                time_no_breathing = 1
            
            else: 
                time_no_breathing = 0
        
        data = {'breathing': breathing, 'time_no_breathing': time_no_breathing, 'crying': crying, 'sleeping': sleeping}
    else: 
        line = get_data_baby_monitor(bm, engine)
        keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')
        data = dict(zip(keys, line))
        data['time_no_breathing'] += 1
        data.pop('id')

    insert_baby_monitor(bm, engine, data)
    return data