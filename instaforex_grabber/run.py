import subprocess
import sys
from time import sleep
import os
from datetime import datetime


def collect_all_links(depth, links_to_analyze):
    for currency in links_to_analyze:
        print(currency)
        with open('all_links_{}.txt'.format(currency), 'w') as all_links:
            subprocess.call(['python3', 'click_to_get_info.py',
                            links_to_analyze[currency], depth], stdout=all_links)


def fill_table(links_name_pattern, links_to_analyze):
    for currency in links_to_analyze:
        with open(links_name_pattern.format(currency), 'r') as all_links:
            subprocess.call(['python3', 'fill_table.py',
                            currency], stdin=all_links)


if __name__ == '__main__':

    links_to_analyze = {}
    with open('links_to_analyze.txt', 'r') as initial_links_file:
        line = initial_links_file.readline()
        while line != '\n':
            splet = line.split()
            links_to_analyze[splet[0]] = splet[1]
            line = initial_links_file.readline()
    interval = 20

    time_start = datetime.now()

    running = True
    while running:
        try:
            sleep(interval)
            print('Cycle started. Please, do not interrupt.')

            collect_all_links('0', links_to_analyze)
            print('Collected.')

            for currency in links_to_analyze:
                print(currency)
                subprocess.call(['python3', 'exclude.py', currency])
            print('Excluded.')

            fill_table('links_{}.txt', links_to_analyze)
            print('Filled.')

            for currency in links_to_analyze:
                os.replace('all_links_{}.txt'.format(currency),
                           'to_be_excluded_{}.txt'.format(currency))

            print('Cycle ended. The solution may be closed.')
        except KeyboardInterrupt:
            running = False
