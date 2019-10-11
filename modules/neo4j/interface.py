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


    def get_user(self):
        with self._driver.session() as session:
            user = session.run(
                "match (user:User {is_processed: false, is_being_processed: false}) "
                "with user "
                "limit 1 "
                "set user.is_being_processed = true "
                "return user.screen_name"
            ).single().value()

            return user


    def write_users(self, user_objects):
        with self._driver.session() as session:
            session.run(
                "with [user_object in {user_objects} | user_object] as user_objects "
                "unwind user_objects as user_object "
                "merge (user:User {id: user_object.id}) "
                "set user.name = user_object.name "
                "set user.screen_name = user_object.screen_name "
                "set user.location = user_object.location "
                "set user.url = user_object.url "
                "set user.description = user_object.description "
                "set user.followers_count = user_object.followers_count "
                "set user.friends_count = user_object.friends_count "
                "set user.listed_count = user_object.listed_count "
                "set user.favourites_count = user_object.favourites_count "
                "set user.statuses_count = user_object.statuses_count "
                "set user.created_at = user_object.created_at "
                "set user.is_processed = false "
                "set user.is_being_processed = false ",
                user_objects=user_objects
            )


    def write_followership(self, following, followers_list):
        with self._driver.session() as session:
            session.run(
                "match (a:User {screen_name: {following}}) "
                "with a as following, [follower in {followers} | follower] as followers "
                "unwind followers as follower "
                "create unique (f:User {id: follower})-[:Follows]->(following) ",
                following=following,
                followers=followers_list
            )

    def user_processed(self, user):
        with self._driver.session() as session:
            session.run(
                "match (u:User {screen_name: {user_name}}) "
                "set u.is_processed = true "
                "set u.is_being_processed = false ",
                user_name=user,
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
