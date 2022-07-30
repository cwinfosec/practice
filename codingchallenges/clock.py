#!/usr/bin/env python3
import sys
import time

def show_time(tHour, tMinute, tSecond):
        print("\033[K" + " Current time: {}H:{}m:{}s\r".format(tHour, tMinute, tSecond), end = ' ', flush = True)
        return

def main(hour, minute, second):

        tHour = hour
        tMinute = minute
        tSecond = second

        while True:

                if tSecond == 60:
                        tSecond = 1
                        tMinute += 1

                if tMinute == 60:
                        tMinute = 0
                        tHour += 1

                if tHour == 24:
                        tHour = 0

                show_time(tHour, tMinute, tSecond)
                time.sleep(1)
                tSecond += 1


if __name__ in "__main__":
        hour = int(input("Enter current hour: "))
        minute = int(input("Enter current minute: "))
        second = int(input("Enter current second: "))
        main(hour, minute, second)