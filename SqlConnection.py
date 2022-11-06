import sys
import mariadb
import json


class Sql:
    def __init__(self):
        # get credentials from json file
        with open('sqlConfig.json') as f:
            data = json.load(f)
            self.host = data['host']
            self.user = data['user']
            self.password = data['password']
            self.database = data['database']
            self.port = int(data['port'])

    def connect(self):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def dbConnectAndExecute(self, query, args):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(query, args)
            conn.commit()
            return cur
        except mariadb.Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
            del conn
