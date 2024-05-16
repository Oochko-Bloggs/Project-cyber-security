#!/usr/bin/env python3
import builtwith
import argparse

parser = argparse.ArgumentParser(description="Find out the technology stack of any website, such as CMS etc.")
parser.add_argument('-u', '--url', type=str, metavar='', required=True, help='Website url')
args = parser.parse_args()
url = args.url

# dictionary type
results = builtwith.builtwith(url)

print(f"Technologies used by {url} :")
for technology, version in results.items():
    print(f"{technology} : {version}")
