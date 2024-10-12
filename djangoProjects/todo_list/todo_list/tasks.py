from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from celery import Celery 

# In Celery, a task is a function that can be executed in the background 
# to define a task, you use the '@shared_task'decorator 
# below function can be executed in the background 
@shared_task
def send_reminders():
    # to get all of user objects who need reminders 
    users= User.objects.filter(reminder=True)

    for each_user in users: # to send reminders to each user 
        send_mail(
            subject= 'Reminder: Your appointment is tomorrow',
            message= 'Dear {}, \n   Please do not forget your appointment tomorrow'.format(each_user.name),
            from_email='kagan12374@outlook.com',
            recipient_list=[each_user.email]
        )

    print("Reminders sent") 


# this line involves the asynchronous execution of the 'send_reminders' function
# (questa riga prevede l'esecuzione asincrona della funzione 'send_reminders')
# send_reminders task is run in the background 
# Celery adds the task to a message broker 
# when you run a task using 'apply_async', Celery adds the task to a message broker, such as Redis
# the message broker acts as a queue, holding the task until it is consumed by a Celery worker process

# in this line, send_reminders task is run in the background 
# and the apply_async method returns an AsyncResult object, which can be used to retrieve the result of the task 

result= send_reminders.apply_async()

# Celery adds the task to a message broker 
# the message broker acts as a queue, holding the task until it is consumed by a Celery 
# when the task is consumed by a Celery worker process, the task is executed in the background 


celery=Celery() # to define object 
# celery determines that adding task to a message broker for different output targets 
celery.send_reminders.apply_asynch()

# a Celery worker process consumes the task from the message broker(place to storage of the send_reminders function)
# to clarify the structure of the instructions 
calculations_of_worker= celery.Worker()
calculations_of_worker.consume_task(send_reminders)

# the Celery worker process executes the code in the task function 
calculations_of_worker.execute_task(send_reminders)

# the Celery worker process returns the result of the task to the message broker 
result=calculations_of_worker.get_result()

# this application retrieves the result of the task using Celery's AsyncResult object 
result= send_reminders.apply_asynch().get()
print(result) # prints the result of the task 

