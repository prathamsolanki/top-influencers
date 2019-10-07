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




if __name__ == "__main__":
    neo4j = Neo4j(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="neo4j",
    )

    print(neo4j.get_lastId())

    neo4j.close()
