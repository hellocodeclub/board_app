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
    return status_order[status_position+1]