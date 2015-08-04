import requests
import re
import csv
from multiprocessing import Pool, cpu_count, freeze_support
import os
import csv
import sys
from domains import *


# domains=[domain.strip() for domain in open('ssl_enabled.txt').read.split()]

def test_url(url):
    def check_ban(url):
        try:
            r=requests.get(url,timeout=10)
            if len(r.text)<=500:
                rv= 'Blocked'
            else:
                rv= 'Not Blocked'
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except :
            rv= 'No SSL' if url.startswith('https') else 'ERROR'
    #     print rv
        return rv
    http_url='http://{}'.format(url)
    https_url='https://{}'.format(url)
    rv= url,check_ban(http_url),check_ban(https_url)
    print '\n**********************\nDomain: {}\nhttp: {}\nhttps: {}\n**************************\n'.format(*rv)
    return rv

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    domains=[part for part in open(resource_path('dump.txt')).read().split() if len(part)>5]
    p=Pool(cpu_count()*2)
    freeze_support()
    # domains=[part for part in open('dump.txt').read().split() if len(part)>5]
    p=Pool(cpu_count()*3)
    try:
        results=p.map(test_url, domains)
    except:
        sys.exit(1)

    headers=['Domain','HTTP','HTTPS']

    with open('report_ssl.csv','w') as csvfile:
        writer=csv.writer(csvfile,dialect='excel')
        writer.writerow(headers)
        writer.writerows(results)

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        freeze_support()
    main()
