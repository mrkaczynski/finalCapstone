# CAPSTONE
# note usernames and paswords are not casesensitive just for ease of use

from datetime import date
from datetime import datetime
from dateutil import parser
from tabulate import tabulate
from dataclasses import dataclass,field

# Task dataclass to handle tasks
@dataclass
class Task:
    assigned_to: str
    task: str
    description: str
    date_assigned: str
    due_date: str
    completed: str

    #method to mark task as completed
    def mark_as_completed(self):
        self.completed = 'Yes'

#to handle task stats in a single object
@dataclass
class TaskOverview:
    task_total: int
    task_completed: int
    task_uncompleted: int
    task_overdue: int
    uncompleted_percentage: int = field(init=False)
    overdue_percentage: int = field(init=False)

    def __post_init__(self):
        self.uncompleted_percentage: int = round((self.task_uncompleted/self.task_total)*100,2)
        self.overdue_percentage: int = round((self.task_overdue/self.task_total)*100,2)

#dictonary to hold user data and list for tasks
validusers = {}
tasks = []

#take data from files
with open("user.txt", 'r+') as form:
    for line in form:
        validusers[line.split(', ')[0]] = line.split(', ')[1].strip('\n')

with open('tasks.txt', 'r+') as form:
    for line in form:
        tasks.append(Task(
            assigned_to = line.split(', ')[0],
            task = line.split(', ')[1],
            description = line.split(', ')[2],
            date_assigned = line.split(', ')[3],
            due_date = line.split(', ')[4],
            completed = line.split(', ')[5].strip('\n')
        ))

#login loop
def login():
    print('''\nTASK MANAGER
    Please provide your username and password''')

    while True:
        user = input("\nUSER: ").lower()
        password = input("\nPASSWORD: ").lower()
    
        # Check input against data from file, display relevant error and loop if incorrect
        while user not in validusers:
            print('\nLOGIN FAILED, USERNAME NOT RECOGNIZED PLEASE RETRY')
            user = input("\nUSER: ").lower()
            password = input("\nPASSWORD: ").lower()

        # check if password matches username
        if password == validusers[user]:
            print('\nSUCCESSFUL LOGIN')
            taskmanager(user = user)
        else:
            print('\nLOGIN FAILED, INCORRECT PASSWORD')

#task menu
def taskmanager(user):

    while True:
        if user == 'admin':
            menu = input('''\nSelect one of the following Options below:
        r - Registering A User
        gr - Generate Reports
        ds - Display User Statistics
        a - Adding A Task
        va - View All Tasks
        vm - View My Tasks
        e - Exit To Login
        : ''').lower()
        else:
            menu = input('''\nSelect one of the following Options below:
        a - Adding A Task
        va - View All Tasks
        vm - View My Tasks
        e - Exit To Login
        : ''').lower()

        if menu == 'r' and user == 'admin':
            reg()
        elif menu == 'ds' and user == 'admin':
            stats()
        elif menu == 'gr' and user == 'admin':
            reports()
        elif menu == 'a':
            add()
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine(user = user)
        elif menu == 'e':
            print("\nGoodbye!!!")
            login()
        else:
            print("\nYou have made a wrong choice, Please Try again")

#register new users
def reg():
    print('\nWelcome to User Registration')

    while True:
        newusername = input('\nPlease provide a username: ').lower()

        if newusername in validusers.keys():
            print('\nThat username is already taken. Please try again.')
            continue
    
        newuserpassword = input('\nPlease provide a password: ').lower()
        passwordcheck = input('\nPlease confirm password given: ').lower()
                
        while newuserpassword != passwordcheck: 
            passwordcheck = input('\nConfirming password failed, please retry: ').lower()

        validusers[newusername] = newuserpassword
        with open('user.txt', 'a+') as form:
            form.write(f'\n{newusername}, {newuserpassword}')
        print('\nUSER ADDED')
        return

#add a task
def add():
    print('\nWelcome to adding a Task')
    today = date.today()
    currentdate = today.strftime('%d %b %Y')

    while True:
        username = input('\nWho would you like to assign the task to, please enter username: ').lower()
        tasktitle = input('\nWhat task are you assigning: ')
        description = input('\nPlease give a short description of this task: ')
        due = parser.parse(input("\nWhen is this task due: "))
        due_final = due.strftime('%d %b %Y')
        no = 'No'

        tasks.append(Task(username, tasktitle, description, currentdate, due_final, no))
        with open('tasks.txt', 'a+') as form:
            form.write(f'\n{username}, {tasktitle}, {description}, {currentdate}, {due_final}, {no}')
            
        print('\nTask Added')

        check = input('\nWould you like to continue to add tasks to file. Yes to continue: ').lower()

        if check != 'yes':
            break

#view all tasks
def view_all():
    print('\nYou have chosen to view all tasks. The following are all tasks on system')
    print(tabulate(tasks, tablefmt='psql', headers='keys', showindex=True))

#view my tasks
def view_mine(user):
    print('\nThe following are all tasks assigned to you')
    #create a list of tasks assigned to this specific user and display it
    my_tasks = [tasks for tasks in tasks if tasks.assigned_to == user]
    print(tabulate(my_tasks, tablefmt='psql', headers='keys', showindex=True))

    #allow user to specify which task they want to edit
    edit = int(input('\nIf you would like to edit a task please enter the number of that task or enter -1 to exit: '))

    if edit != -1:
        name_complete = input('\nWould you like to mark the task complete or change who the task is assigned to, enter either mark/assignment: ').lower()
        
        #edit task accordingly and display it
        if name_complete == 'mark':
            Task.mark_as_completed(my_tasks[edit])
            print(tabulate(my_tasks, tablefmt='psql', headers='keys', showindex=True))
        elif name_complete == 'assignment':
            my_tasks[edit].assigned_to = input('\nPlease enter username who you would like to assign the task to: ')
            print(tabulate(my_tasks, tablefmt='psql', headers='keys', showindex=True))

    else:
        return

#see stats
def stats():
    #run overview to make reports, see_data to differentiate from reports function
    see_data = 'yes'
    overview(see_data)

#generate reports
def reports():
    #run overview to make reports, see_data to differentiate from stats function
    see_data = 'no'
    overview(see_data)

#make reports
def overview(see_data):
    #task overview
    t_overview = []
    t_overview.append(TaskOverview(
    task_total = len(tasks),
    task_completed = len([task for task in tasks if task.completed == 'Yes']),#create a list of completed tasks and take length
    task_uncompleted = len([task for task in tasks if not task.completed == 'Yes']),#create a list of non-completed tasks and take length
    task_overdue = len([task for task in tasks if task.due_date < str(datetime.date) and not task.completed == 'Yes'])#create a list of tasks where date today has exceeded due date and take length
    ))

    with open('task_overview.txt', 'w+') as form:
        form.write(tabulate(t_overview, tablefmt='psql', headers='keys'))

    #user overview
    u_overview = {}
    
    validusers_list = [key.split(', ') for key in validusers.keys()] #so i can manipulate the users list by index

    u_overview['total_users'] = len(validusers_list)
    u_overview['total_tasks'] = len(tasks)

    #https://plainenglish.io/blog/how-to-dynamically-declare-variables-inside-a-loop-in-python
    #do the calculations for each user and add them to a dictionary
    for x, user in enumerate(validusers_list):
        name = str(validusers_list[x])
        user_tasks = len([task for task in tasks if task.assigned_to in str(validusers_list[x])])
        comparison = round((user_tasks / len(tasks))*100, 2)
        user_completed = round(len([task for task in tasks if task.assigned_to in str(validusers_list[x]) and task.completed == 'Yes'])/user_tasks*100, 2)
        user_uncompleted = 100 - user_completed
        overdue = round(len([task for task in tasks if task.assigned_to in str(validusers_list[x]) and task.completed == 'No' and task.due_date < str(datetime.date)])/user_tasks*100, 2)
        u_overview[name] = [(f'User Tasks: {user_tasks}'), (f'Percentage of Total Tasks: {comparison}'), (f'Percentage Completed: {user_completed}'), (f'Percentage Uncompleted: {user_uncompleted}'), (f'Percentage Overdue: {overdue}')]

    with open('user_overview.txt', 'w+') as form:
        form.write(str(u_overview))

    if see_data == 'yes':
        return print(tabulate(t_overview, tablefmt='psql', headers='keys')), print(u_overview)
    else:
        return

login()
