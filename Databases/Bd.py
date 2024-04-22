from mysql.connector.aio import connect
from mysql.connector.errors import DatabaseError
import asyncio
import nest_asyncio
from pydantic import SecretStr
from aiogram.fsm.context import FSMContext
from bot_config import config


class SingletonBd(object):
    __instance = None
    __mydb = None
    tables = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.tables = args[0]
        return cls.__instance

    async def bd_connect(self, user: SecretStr, password: SecretStr, port: int, database: str, host: str):
        try:
            self.__mydb = await connect(
                user=user.get_secret_value(),
                port=port,
                database=database,
                host=host,
                password=password.get_secret_value()
            )
            print('Done')
        except Exception as e:
            print(e)
            raise DatabaseError('not connection')

    async def select_bg(self, str_query: str):
        cursor = await self.__mydb.cursor()
        await cursor.execute(str_query)
        answer = await cursor.fetchall()
        await cursor.close()
        return answer

    async def insert_bd(self, str_query: str):
        cursor = await self.__mydb.cursor()
        await cursor.execute(str_query)
        await self.__mydb.commit()
        await cursor.close()

    async def describe_table(self):
        cursor = await self.__mydb.cursor()
        answer = {}
        for i in self.tables:
            await cursor.execute(f'DESCRIBE {i};')
            answer[i] = tuple(map(lambda x: x[0:2], await cursor.fetchall()))
        await cursor.close()
        return answer
