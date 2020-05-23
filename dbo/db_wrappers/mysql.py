import asyncio
import mysql.connector

class MysqlConnector:
    """Mysql connector async wrapper
    
    TODO: this is a naive implementation, either to be replaced by another library or have
    its functionaly extended
    """
    def __init__(self, connection):
        """initialize a new connection"""
        self.c = mysql.connector.connect( **connection);
    
    async def invoke(self, query):
        """execute SQL queries in the async loop, then return the query cursor"""
        cursor = self.c.cursor(buffered=True)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, cursor.execute, query)
        await loop.run_in_executor(None, self.c.commit)
        return cursor