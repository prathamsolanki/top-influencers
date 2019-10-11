import time
from multiprocessing import Process
from modules.lib.get_users_from_tweets import GetUsers
from modules.lib.get_followers import GetFollowers

credentials = [
    'credentials_pratham.json',
    'credentials_edo.json',
]


get_users = Process(target=GetUsers.run, args=(credentials,))
get_users.start()

p = []
for i in range(0, len(credentials)):
    p.append(Process(target=GetFollowers.run, args=(credentials[i],)))
    p[i].start()
    