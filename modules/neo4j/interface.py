from neo4j import GraphDatabase
import time

class Neo4j:
    def __init__(self, uri, user, password):
        """
        Opening the session to Neo4j
        """
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self, ):
        self._driver.close()

    
    def init_execution(self, ):
        """
        Write some stats regarding the initial time of execution
        This is useful if we finish the limit of 7 days,
        so we know at which time we started 
        """
        now = int(round(time.time() * 1000))

        with self._driver.session() as session:
            session.run(
                "create (node:Execution {startedAt: {now}})",
                now=now
            )
    

    def get_lastId(self, ):
        """
        Getting the last_id for retrieving tweets
        """
        with self._driver.session() as session:
            last_id = session.run(
                "match (x:Execution) "
                "return x.last_id "
                "order by x.startedAt desc "
                "limit 1"
            ).single().value()
            
            return last_id

    def write_lastId(self, last_id):
        """
        Update the value for the last_id
        """
        # Get the most recent execution
        with self._driver.session() as session:
            session.run(
                "match (x:Execution) "
                "with x "
                "order by x.startedAt desc "
                "limit 1 "
                "set x.last_id = {last_id}",
                last_id=last_id
            )


<<<<<<< HEAD
    def get_users(self):
=======
    def get_user(self):
>>>>>>> 81acb2fcca5e5d97deefed04c233368b1c03e316
        with self._driver.session() as session:
            users = session.run(
                "match (:User {is_processed: false}) as user "
                "with user "
                "limit 1 "
                "set user.is_processed = true "
                "return user.screen_name"
            )

            return users


    def write_users(self, user_objects):
        with self._driver.session() as session:
            session.run(
                "using periodic commit 500 "
                "with [user_object in {user_objects} | user_object] as user_objects "
                "unwind user_objects as user_object "
                "merge (:User {id: user_object.id, name: user_object.name, screen_name: user_object.screen_name, location: user_object.location, url: user_object.url, description: user_object.description, followers_count: user_object.followers_count, friends_count: user_object.friends_count, listed_count: user_object.listed_count, favourites_count: user_object.favourites_count, statuses_count: user_object.statuses_count, created_at: user_object.created_at, is_processed: false})",
                user_objects=user_objects
            )


    def write_followership(self, following, followers_list):
        with self._driver.session() as session:
            session.run(
                "using periodic commit 500 "
                "match (a:User {id: {following.id}}) "
                "with a as following, [follower in {followers} | follower] as followers "
                "unwind followers as follower "
                "create unique (f:User {id: follower.id, name: follower.name, screen_name: follower.screen_name, location: follower.location, url: follower.url, description: follower.description, followers_count: follower.followers_count, friends_count: follower.friends_count, listed_count: follower.listed_count, favourites_count: follower.favourites_count, statuses_count: follower.statuses_count, created_at: follower.created_at, is_processed: true}) - [:follows] -> (following)",
                following=following,
                followers_list=followers_list
            )


    def test(self, list_param):
        with self._driver.session() as session:
            result = session.run(
                "return [x in {list_param} | x.name] as result",
                list_param=list_param
            )
            print(result.single().value())


if __name__ == "__main__":
    neo4j = Neo4j(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="neo4j",
    )

    neo4j.test([{'name': 'hello'}, {'name': 'how are you?'}])

    neo4j.close()
