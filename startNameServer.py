import socket
import Pyro5.nameserver

def main():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ns = Pyro5.nameserver.start_ns_loop(host=ip_address)
    print("Name server started on", ip_address)
    print(ns)

if __name__ == "__main__":
    main()