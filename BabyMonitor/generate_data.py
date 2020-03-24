from sqlalchemy.sql import select
import random
import model_baby_monitor
import sys
sys.path.append('../')
from construct_scenario import *

crying = False
sleeping = True
breathing = True
time_no_breathing = 0
max_no_changes = random.randint(5,15)


def count(function):
    
    def wrapped(monitor, flag):
        
        global max_no_changes, breathing

        if flag == -1: 
            wrapped.calls = 0
            max_no_changes = random.randint(3, 5)
            return(flag, monitor)


        if wrapped.calls < max_no_changes:
            wrapped.calls += 1
            if wrapped.calls == 1:  
                return function(0, monitor)
            elif breathing:
                return 1 
            else: 
                return function(wrapped.calls, monitor)

        else:        
            wrapped.calls = 0 
            max_no_changes = random.randint(3,5)
            return function(0, monitor)
    
    wrapped.calls = 0
    return wrapped

@count
def data_from_baby(flag, monitor):
    global crying, sleeping, breathing, time_no_breathing

    data = {}

    if flag == -1: 
        crying = False
        sleeping = random.choices([True, False], [0.75, 0.25], k = 1)[0]
        breathing = True
        time_no_breathing = 0
        data = {'breathing': breathing, 'time_no_breathing': time_no_breathing, 'crying': crying, 'sleeping': sleeping}

        print("Reseta dados ", data)

    elif flag == 0:   
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

            if sleeping:
                crying = False

            else: 
                time_no_breathing = 0
            
        data = {'breathing': breathing, 'time_no_breathing': time_no_breathing, 'crying': crying, 'sleeping': sleeping}
        
        print("Gera novos dados ", data)

    else: 
        line = monitor.get_data_baby_monitor()
        keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')
        data = dict(zip(keys, line))
        data['time_no_breathing'] += 1
        data.pop('id')
        print('Altera respiração ', data)

    monitor.insert_baby_monitor(data)
    
    return data