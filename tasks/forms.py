from board.constants import *
class TaskForm:
    def __init__(self,postRequest):
        self.taskId = postRequest.POST.get(TASK_FORM_ID)
        self.titleName = postRequest.POST[TASK_FORM_NAME]
        self.projectId = postRequest.POST.get(TASK_FORM_PROJECT)
        self.estimatedHours = postRequest.POST.get(TASK_FORM_ESTIMATED_HOURS) if postRequest.POST.get(TASK_FORM_ESTIMATED_HOURS) else 1
        self.assignedPerson = postRequest.POST.get(TASK_FORM_ASSIGNED_PERSON)
        self.status =postRequest.POST[TASK_FORM_STATUS] if postRequest.POST[TASK_FORM_STATUS] else 'OPEN'
        self.include_to_current_cycle = postRequest.POST.get(TASK_FORM_INCLUDE_IN_CURRENT_CYCLE)
        self.description = postRequest.POST[TASK_FORM_DESCRIPTION]

