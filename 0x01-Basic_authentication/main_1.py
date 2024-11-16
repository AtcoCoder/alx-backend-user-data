#!/usr/bin/python3
""" Check response
"""
import requests

if __name__ == "__main__":
    url = 'http://0.0.0.0:5000/api/v1/unauthorized/'
    import time

    r = ''
    while r == '':
        try:
            r = requests.get(url)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    if r.status_code != 401:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
   
    print("OK", end="")
