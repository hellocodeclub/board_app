status_choices = {
    'open':'Open',
    'ready':'Ready To Start',
    'in_progress':'In Progress',
    'test':'Check It Works',
    'done':'Done'
}

status_order = ['OPEN','READY','IN_PROGRESS','TEST','DONE']

def next_state(status):
    status_position = status_order.index(status.upper())
    if(status_position+1>len(status_choices)-1):
        return len(status_choices)-1
    return status_order[status_position+1]

def previous_state(status):
    status_position = status_order.index(status.upper())
    if(status_position-1<0):
        return 0
    else:
        return status_order[status_position-1]