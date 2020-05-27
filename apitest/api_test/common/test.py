#! /usr/bin/python

from threading import Thread
import time
import re

def my_counter():
    i = 0
    for _ in range(100000000):
        i = i + 1
    return True

def single():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))

def multiple():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    # single()
    # reg="验证(?P<locator>.*)为(?P<expected>.*)"
    reg="验证(?P<locator>.*)为(?P<expected>.*)"
    str="验证code为0"
    code=""
    expected=""
    try:
        match=re.search(reg,str)
        if match:
            code=match.group(1)
            expected=match.group(2)
            print(code)
            print(expected)
    except Exception as e:
        print(str(e))