#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
import argparse
import subprocess
from urllib.parse import urlparse

roadmap = {
	"_youtube.com": ["/usr/bin/smplayer"],
	"youtu.be":     ["/usr/bin/smplayer"],
	"rest":         ["/usr/bin/vivaldi", "--force-dark-mode"],
} # - = - = - = - = ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ = - = -
# u can specify prescribed special flags for some applications

# PARSE FLAGS. Extract the URL and ignore the rest of the flags.
parser = argparse.ArgumentParser()
parser.add_argument('url', help='URL to process')

args, unknown = parser.parse_known_args()
url = args.url

print(f'URL: {url}')
print(f'Unused flags: {str(unknown)}')

# Parse URL
urlparse_result = urlparse(url)
print(urlparse_result)
domain = urlparse_result[1] # extract netloc=

# Just remove www. to simplify parsing
if domain[0:4] == "www.":
	domain = domain[4:]

print(f"Detected domain: {domain}")

def roadmap_url(domain):
	"""
	Specifically sets specific rules for domains and distributes automated ones via roadmap.
	Placed in a function for convenience
	"""

	# - = - = FILTER (www.)youtube.com/(watch|playlist) ONLY. For example youtube.com/user redirects in browser.
	if domain in ("www.youtube.com", "youtube.com") and "_youtube.com" in roadmap:
		path = urlparse_result[2] # extract path=
		if path in ("/watch", "/playlist") or path[0:7] == "/shorts":
			return roadmap["_youtube.com"]
		del path
		# else: pass
	# - = - = - = - = - = - = - = - = - = - = - = 

	if domain in roadmap:
		return roadmap[domain]
	return roadmap["rest"]

open_with = roadmap_url(domain)

# and just start binary!:)
print(f"Launch Options: {str(open_with+[url])}")
subprocess.Popen(open_with+[url]) # +unknown (?)
