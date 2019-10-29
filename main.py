import time
import sys
from multiprocessing import Process
from modules.lib.get_users_from_tweets import GetUsers
from modules.lib.get_followers import GetFollowers

credentials = [
    'credentials_pratham.json',
    'credentials_edo.json',
]


if (len(sys.argv) > 1) and (sys.argv[1] == "initial"):
    initial_run = True
else:
    initial_run = False

get_users = Process(target=GetUsers.run, args=(credentials, initial_run))
get_users.start()

if not initial_run:
    p = []
    for i in range(0, len(credentials)):
        p.append(Process(target=GetFollowers.run, args=(credentials[i],)))
        p[i].start()
    
