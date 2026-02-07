# Copyright [2026] [Mattia Barbero]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mysql.connector
from mysql.connector import errorcode
import pathlib

class DBConnect:
    """Class that is used to create and manage a pool of connections to the database.
    It implements a class method that works as a factory for lending the connections from the pool"""
    # we keep the pool of connections as a class attribute, not an instance attribute
    _cnxpool = None

    def __init__(self):
        raise RuntimeError('Do not create an instance, use the class method get_connection()!')

    @classmethod
    def get_connection(cls, pool_name = "my_pool", pool_size = 3) -> mysql.connector.pooling.PooledMySQLConnection:
        """Factory method for lending connections from the pool. It also initializes the pool
        if it does not exist
        :param pool_name: name of the pool
        :param pool_size: number of connections in the pool
        :return: mysql.connector.connection"""
        if cls._cnxpool is None:
            try:
                cls._cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=pool_name,
                    pool_size=pool_size,
                    option_files=f"{pathlib.Path(__file__).resolve().parent}/connector.cnf"
                )
                return cls._cnxpool.get_connection()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                    return None
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                    return None
                else:
                    print(err)
                    return None
        else:
            return cls._cnxpool.get_connection()