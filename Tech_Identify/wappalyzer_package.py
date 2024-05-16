#!/usr/bin/env python3
from wappalyzer import Wappalyzer, WebPage
import argparse

parser = argparse.ArgumentParser(description="Find out the technology stack of any website, such as the CMS etc.")
parser.add_argument('-u', '--url', type=str, metavar='', required=True, help='Website url')
args = parser.parse_args()
url = args.url

wappalyzer = Wappalyzer.latest()
webpage = WebPage.new_from_url(url)
print(wappalyzer.analyze(webpage))
