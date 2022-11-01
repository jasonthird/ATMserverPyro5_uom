import Pyro5.api
import mariadb
from decimal import *
import sys

getcontext().prec = 13 + 4
try:
    conn = mariadb.connect(
        user="root",
        password="",
        host="",
        port=3306,
        database="atm"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

@Pyro5.api.expose
class Atm(object):

    def Auth(self, pin, name):
        cur.execute(
            "SELECT AuthCode from authCode inner join users u on authCode.owner_id = u.id where u.id = authCode.owner_id and u.pin = ? and u.username = ?",
            (pin, name))
        return cur.next()

    def getBalance(self, Authcode):
        cur.execute(
            "select balance from balances inner join authCode aC on balances.owner_id = aC.owner_id where AuthCode=?"
            , (Authcode,))
        return cur.next()

    def deposit(self,auth,value):
        money = Decimal(value)
        cur.execute("UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id set balance = balance + ? where AuthCode=?",
                    (money,auth,))
        return 0 #0 is for ok

    def withdraw(self,auth,value):
        money = Decimal(value)
        cur.execute("""UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id
                set balance =
                CASE
                    WHEN balance - ? >= 0. then balance - ?
                else balance
            End
            where AuthCode=?""",(money,money,auth))
        return 0


daemon = Pyro5.server.Daemon()  # make a Pyro daemon
ns = Pyro5.api.locate_ns()  # find the name server
uri = daemon.register(Atm)  # register the greeting maker as a Pyro object
ns.register("example.Atm", uri)  # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()  # start the event loop of the server to wait for calls
