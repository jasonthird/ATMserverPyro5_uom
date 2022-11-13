import Pyro5.api
from decimal import *
import sys

import SqlConnection

getcontext().prec = 13 + 4


def main():
    sql = SqlConnection.Sql()

    @Pyro5.api.expose
    class Atm(object):
        def Auth(self, pin, name):
            try:
                cur = sql.dbConnectAndExecute(
                    """SELECT AuthCode from authCode inner join users u on authCode.owner_id = u.id 
                    where u.id = authCode.owner_id and u.pin = ? and u.username = ?""",
                    (pin, name))
                answer = cur.next()
                if answer is None:
                    return "Invalid credentials"
                else:
                    return answer[0]
            except Exception:
                return "backend error"

        def getBalance(self, Authcode):
            try:
                cur = sql.dbConnectAndExecute(
                    "select balance from balances inner join authCode aC on balances.owner_id = aC.owner_id where AuthCode=?"
                    , (Authcode,))
                if cur is None:
                    return "Invalid credentials"
                else:
                    return cur.next()[0]
            except Exception:
                return "backend error"

        def deposit(self, auth, value):
            try:
                money = Decimal(value)
                current_money = Decimal(self.getBalance(auth))
                cur = sql.dbConnectAndExecute(
                    """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id 
                    set balance = IF(?>0, balance + ?, balance)
                    where AuthCode=?
                    """,
                    (money, money, auth,))
                # check if the change was made
                if self.getBalance(auth) == current_money:
                    return "Invalid input"  # failed due to invalid arguments
                return "Success"
            except Exception:
                return "backend error"

        def withdraw(self, auth, value):
            try:
                money = Decimal(value)
                current_money = Decimal(self.getBalance(auth))
                cur = sql.dbConnectAndExecute(
                    """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id
                        set balance =
                        IF(balance - ?>= 0., IF(? >= 0., balance - ?, balance), balance)
                    where AuthCode=?""", (money, money, money, auth,))
                # check if the change was made
                if self.getBalance(auth) == current_money:
                    return "Invalid input"
                else:
                    return "Success"
            except Exception:
                return "backend error"

    daemon = Pyro5.server.Daemon()  # make a Pyro daemon
    ns = Pyro5.api.locate_ns()  # find the name server
    uri = daemon.register(Atm)  # register the greeting maker as a Pyro object
    ns.register("example.Atm", uri)  # register the object with a name in the name server
    name = ns.lookup("example.Atm")
    print("Name of the object:", ns.list(prefix="example.Atm"))
    print("if running on a different machine, use the ip address of the server")
    print("but first try PYRONAME:example.Atm")
    daemon.requestLoop()  # start the event loop of the server to wait for calls


# for testing
def createDb():
    sql = SqlConnection.Sql()
    sql.createDb()


def createTables():
    sql = SqlConnection.Sql()
    sql.createTables()


def insertTestData():
    sql = SqlConnection.Sql()
    sql.insertTestData()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "createDb":
            try:
                createDb()
            except Exception as e:
                print(e)
        elif sys.argv[1] == "createTables":
            try:
                createTables()
            except Exception as e:
                print(e)
        elif sys.argv[1] == "insertTestData":
            try:
                insertTestData()
            except Exception as e:
                print(e)
        elif sys.argv[1] == "setupDb":
            try:
                createDb()
                createTables()
                insertTestData()
            except Exception as e:
                print(e)
    else:
        main()  # start the server
