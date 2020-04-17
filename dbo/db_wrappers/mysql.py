import asyncio
import mysql.connector

class MysqlConnector:
    def __init__(self, connection):
        self.c = mysql.connector.connect( **connection);
    
    async def invoke(self, query):
        cursor = self.c.cursor(buffered=True)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, cursor.execute, query)
        await loop.run_in_executor(None, self.c.commit)
        return cursor