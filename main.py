import common as c
import testcases as tc
import threading
import time
import random
import argparse

@c.pre_main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help = "show all test scripts", action = "store_true")
    parser.add_argument("-r", "--run", help = "run specific test script")

    args = parser.parse_args()

    if args.list == True:
        tests = tc.list_testscripts()
        for i in tests:
            print(i) 

    if args.run != None:
        tc.run(args.run)

if __name__ == '__main__':
    main()