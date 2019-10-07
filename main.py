import time

from modules.lib.get_users_from_tweets import GetUsers

credentials = [
    'credentials_pratham.json',
    'credentials_edo.json',
]

# Initial run
# get_users = GetUsers(credentials=credentials[0])
# get_users.run(initial_run=True)
# get_users.close()

while True:
    for c in credentials:
        get_users = GetUsers(credentials=c)
        get_users.run()
        get_users.close()

    # sleep for 10 seconds
    time.sleep(10)
    