# ATM tellel machine server using pyro5
Exercise for the distributed programming course in university of macedonia

## Python3 dependences 
mariadb Pyro5
  
## Usage
Given that you have access to a mariadb instance, modify the sqlConfig.json to configure the database connection.
<br>
If you are running it for the first time and need to set the database up just run
``` python3 main.py setupDb```. This will automatically connect to mariadb and create and setup a database (name specified in sqlConfig.json) with some test data.
<br>
After that make sure that you have a pyro5 nameserver running. For ease of use just run ```python3 startNameServer.py``` to start it. It should bind it to the correct ip address and make it accessible to lan.
<br><br>Finally run ```python3 main.py``` to start the server.

