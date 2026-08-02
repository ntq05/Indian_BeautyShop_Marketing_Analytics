import os 
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus

class DatabaseConnector:
    def __init__(self, env_path: str = ".env"):

        load_dotenv(env_path, override=True)
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        self._engine: Engine = None

    def get_engine(self) -> Engine:
        if self._engine is None:

            print("host =", repr(self.db_host))
            print("user =", repr(self.db_user))
            print("password =", repr(self.db_password))

            url = URL.create(
                drivername="mysql+pymysql",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=int(self.db_port),
                database=self.db_name,
            )
            print(url)
            self._engine = create_engine(
                url,
                pool_pre_ping=True, #Added to check if the connection is alive before using it
                pool_size = 5, #Added to set the maximum number of connections in the pool
                max_overflow = 10, #Added to set the maximum number of connections that can be created after the pool is full
            )

        return self._engine

    def query(self, sql_query: str, params: dict = None) -> pd.DataFrame:
        """
        param sql_query: The SQL query to execute.
        param params: Optional dictionary of parameters to pass to the SQL query.
        return: A pandas DataFrame containing the results of the query.
        """

        engine = self.get_engine()

        return pd.read_sql_query(sql_query, engine, params=params)

    def close(self):
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            print("Database connection closed.")