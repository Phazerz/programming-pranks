#!/usr/bin/env python

# from osascript import osascript
from time import sleep
from subprocess import check_call
import argparse


def escape_string(string):
    """Take a string and return a version that escapes backslashes and quotes.

    """
    return string.replace("\\", "\\\\").replace('"', '\\"')


def run_applescript(script, **kwargs):
    """Run a string in Applescript, escaping given kwargs for a .format

    """

    fmtargs = {}
    for k, v in kwargs.items():
        fmtargs[k] = escape_string(v)
    script = script.format(script, **fmtargs)
    check_call(['osascript', '-e', script])
    # returncode, stdout, stderr = osascript(script)
    # if returncode != 0:
    #     raise SystemError(
    #         "Error running Applescript (error code {}): '{}'".format(
    #             returncode, stderr))
    # return stdout


def text_person(person, text):
    """Text a specific person the given text"""
    run_applescript(
        'tell application "Messages" to send "{text}" to buddy "{person}"',
        text=text, person=person)


def split_file(f):
    for line in f:
        line = line.strip()
        if line:
            yield line


def nuke(person, f, sleep_time=30):
    for text in split_file(f):
        text_person(person, text)
        sleep(sleep_time)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "person",
        help="Person to be texted")
    parser.add_argument(
        "filename",
        help="Name of the file to be nuked")
    parser.add_argument(
        "--sleeptime",
        help="Number of seconds between texts [default 30]",
        type=float,
        default=30.0)
    args = parser.parse_args()
    with open(args.filename) as f:
        nuke(args.person, f, args.sleeptime)


if __name__ == '__main__':
    main()







