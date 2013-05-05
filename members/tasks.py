from datetime import *

# from celery.decorators import task
from djcelery import celery
from mailsnake import *

import mijnhercules.settings.base as settings
from .models import Player


# map email user to player.


# @task
# @celery.task
# def log_mailchimpexceptions(*args):
#     ms = MailSnake(settings.MAILCHIMP_API)
#     # pl = Player.objects.all()
#     pl = Player.objects.filter(email='bteeuwen@gmail.com')
#     exceptions = {}
#     exceptions['emaillessplayers'] = []
#     emaillessplayers = 0
#     for p in pl:
#         if p.email:
#             try:
#                 status = ms.listMemberInfo(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address = p.email)['data'][0]['status']
#                 # if status != 'subscribed':
#                 exceptions[p.email] = status    
#             except:
#                 exceptions[p.email] = 'Failed'
#         elif not p.email:
#             exceptions['emaillessplayers'].append(p)
#     def timestamp():
#         '''Function to create datetime object to string.'''
#         dt_obj = datetime.now()
#         date_str = dt_obj.strftime("%Y%m%d%H%M%S")
#         return date_str

#     filename = settings.SITE_ROOT + '/scripts/logs/mailchimp_fouten_' + timestamp() + ".txt"
#     out_file = open(filename, "w")
#     for k, v in exceptions.iteritems():
#         print k, v
#         out_file.write(k, v + '\n')
#     out_file.close()
#     return True


 
# @celery.task
# def add(x,y):
#     return x + y
 
# @celery.task
# def sleeptask(i):
#     from time import sleep
#     sleep(i)
#     return i