import asyncpg

class Database:
        def __init__(self, user, password, database, host='localhost', port=5432):
                self.user = user
                self.password = password
                self.database = database
                self.host = host
                self.port = port
        async def connect(self):
                self.pool = await asyncpg.create_pool(
                        user=self.user,
                        password=self.password,
                        database=self.database,
                        host=self.host,
                        port=self.port,
                )

        async def disconnect(self):
                self.pool.close()