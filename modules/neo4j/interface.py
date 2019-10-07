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
        Getting teh last_id for retrieving tweets
        """
        return 0

    def write_lastId(self, last_id):
        """
        Update the value for the last_id
        """
        pass


if __name__ == "__main__":
    neo4j = Neo4j(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="neo4j",
    )

    neo4j.init_execution()

    neo4j.close()
