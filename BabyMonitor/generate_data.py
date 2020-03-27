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
max_no_changes = random.randint(3,7)

#flag = -1: bebê está bem
#flag = 0: status novo
#flag >= 1: status sem alteração

def count(function):
    
    def wrapped(monitor, flag):
        
        global max_no_changes, breathing

        if flag == -1: 
            wrapped.calls = 0
            max_no_changes = random.randint(3,7)
            return function(-1, monitor)

        if flag == 0: 
            wrapped.calls += 1
            if wrapped.calls < max_no_changes:
                if wrapped.calls == 1:  
                    return function(0, monitor)
                return function(1, monitor)
            else:        
                wrapped.calls = 0
                max_no_changes = random.randint(5,10)
                return function(0, monitor)
     
        if flag == 1: 
            wrapped.calls += 1
            return function(1, monitor)

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

    elif flag == 0:   
        crying = random.choices([True, False], [0.75,0.25], k=1)[0]

        if crying:
            sleeping = False
            breathing = True
            time_no_breathing = 0 
        
        else: 
            sleeping = random.choices([True, False], [0.75, 0.25], k = 1)[0]
            breathing = random.choices([True, False], [0.75, 0.25], k = 1)[0]

            if not breathing: 
                time_no_breathing = 1

            else: 
                time_no_breathing = 0
            
            if sleeping:
                crying = False

        data = {'breathing': breathing, 'time_no_breathing': time_no_breathing, 'crying': crying, 'sleeping': sleeping}

    else: 
        line = monitor.get_data_baby_monitor()
        keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')
        data = dict(zip(keys, line))
        if not data['breathing']:
            data['time_no_breathing'] += 1
        data.pop('id')

    monitor.insert_baby_monitor(data)
    
    return data