#!/usr/bin/python3

from argparse import ArgumentParser
import socket
from threading import Thread
from time import time
from datetime import datetime
import pyfiglet
import getmac

open_ports = []
service_map = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    23:"TELNET",
    25:"SMPT",
    53: "DNS",
    110:"POP3",
    2049:"NFS",
    995: "POP3s",
    5900:"VNC",
    8080:"HTTP",
    1194:"OPENVPN",
    465:"SMPTS",
    69:"TFTP",
    143:"IMAP",
}

def prepare_args():
    """Prepare arguments"""
    parser = ArgumentParser(description="PYTHON BASED FAST PORT SCANNER", usage="%(prog)s 192.168.1.0/24", epilog="Example - %(prog)s -s 20 -e 40000 -t 2000 -V 192.168.1.0/24")
    parser.add_argument("IP", metavar="IPv4", help="HOST TO SCAN")
    parser.add_argument("-s", "--start", dest="start", metavar="", type=int, help="Starting port", default=1)
    parser.add_argument("-e", "--end", dest="end", metavar="", type=int, help="Ending port", default=65535)
    parser.add_argument("-t", "--threads", dest="threads", metavar="", type=int, help="Threads to use", default=2000)
    parser.add_argument("-T", "--target-time", dest="target_time", metavar="", type=int, help="Scanning target time (seconds)", default=10)
    parser.add_argument("-V", "--verbose", dest="verbose", action="store_true", help="verbose output")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0", help="display version")
    args = parser.parse_args()
    return args

def prepare_ports(start: int, end: int):
    """Generator function for ports"""
    for port in range(start, end+1):
        yield port

def detect_service(port):
    """Detect service running on the given port"""
    if port in service_map:
        return service_map[port]
    else:
        return "Unknown"

def scan_port():
    """Scan Ports"""
    while True:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            port = next(ports)
            s.connect((arguments.IP, port))
            open_ports.append((port, detect_service(port)))
            if arguments.verbose:
                print(f"\r{open_ports}", end="")
        except (ConnectionRefusedError, socket.timeout):
            continue
        except StopIteration:
            break

def prepare_threads(threads: int):
    """Create and start threads"""
    thread_list = []
    for _ in range(threads):
        thread_list.append(Thread(target=scan_port))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    # ASCII Banner
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    target = input("TARGET IP: ")

    # Banner
    print("*" * 100)
    print("Scanning Target: " + target)
    print("Scanning started at: " + str(datetime.now()))
    print("*" * 100)
    arguments = prepare_args()
    ports = prepare_ports(arguments.start, arguments.end)
    start_time = time()
    prepare_threads(arguments.threads)
    end_time = time()
    if arguments.verbose:
        print()
print("MAC ADDRESS OF TARGET:", getmac.get_mac_address(ip=target))  # Print MAC address here    
print("OPEN PORTS FOUND:")
    for port, service in open_ports:
        print(f"Port: {port} - Service: {service}")
        print ("_" * 60)
    print(f"TIME TAKEN - {round(end_time-start_time, 2)} seconds")
