#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
import argparse
import subprocess
from urllib.parse import urlparse

roadmap = {
	"_youtube.com": ["/usr/bin/smplayer"],
	"youtu.be":     ["/usr/bin/smplayer"],
	"rest":         ["/usr/bin/vivaldi", "--force-dark-mode"],
}

# PARSE FLAGS. Extract the URL and ignore the rest of the flags.
parser = argparse.ArgumentParser()
parser.add_argument('url', help='URL to process')

args, unknown = parser.parse_known_args()
url = args.url

print(f'URL: {url}')
print(unknown)

# Parse URL
urlparse_result = urlparse(url)
print(urlparse_result)
domain = urlparse_result[1] # extract netloc=

# Just remove www. to simplify parsing
if domain[0:4] == "www.":
	domain = domain[4:]

print(domain)

def roadmap_url(url):
	if domain == "www.youtube.com" or domain == "youtube.com" and "_youtube.com" in roadmap:
		path = urlparse_result[2] # extract path=
		if path == "/watch" or path == "/playlist":
			return roadmap["_youtube.com"]
		del path
		# else: pass

	if domain in roadmap:
		return roadmap[domain]
	return roadmap["rest"]

open_with = roadmap_url(domain)

# and just start binary!:)
print(open_with+[url])
subprocess.Popen(open_with+[url]) # +unknown (?)