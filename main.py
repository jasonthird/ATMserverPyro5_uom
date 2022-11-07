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
                return cur.next()
            except :
                return "mariadb error"

        def getBalance(self, Authcode):
            cur = sql.dbConnectAndExecute(
                "select balance from balances inner join authCode aC on balances.owner_id = aC.owner_id where AuthCode=?"
                , (Authcode,))
            return cur.next()

        def deposit(self, auth, value):
            money = Decimal(value)
            cur = sql.dbConnectAndExecute(
                """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id 
                set balance = IF(?>0, balance + ?, balance)
                where AuthCode=?
                """,
                (money, money, auth,))
            # check if the change was made
            if self.getBalance(auth) == money:
                return 1  # failed due to invalid arguments
            return 0  # success

        def withdraw(self, auth, value):
            money = Decimal(value)
            cur = sql.dbConnectAndExecute(
                """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id
                    set balance =
                    IF(balance - ?>= 0., IF(? >= 0., balance - ?, balance), balance)
                where AuthCode=?""", (money, money, money, auth,))
            return 0

    daemon = Pyro5.server.Daemon()  # make a Pyro daemon
    ns = Pyro5.api.locate_ns()  # find the name server
    uri = daemon.register(Atm)  # register the greeting maker as a Pyro object
    ns.register("example.Atm", uri)  # register the object with a name in the name server

    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls


if __name__ == "__main__":
    main()
