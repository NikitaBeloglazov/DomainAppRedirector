#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
"""
 * Copyright (C) 2023 Nikita Beloglazov <nnikita.beloglazov@gmail.com>
 *
 * This file is part of NikitaBeloglazov/DomainAppRedirector.
 *
 * NikitaBeloglazov/DomainAppRedirector is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License v3.0
 * published by the Mozilla Foundation.
 *
 * NikitaBeloglazov/DomainAppRedirector is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY.
 *
 * You should have received a copy of the GNU General Public License v3.0
 * along with NikitaBeloglazov/DomainAppRedirector
 * If not, see https://www.gnu.org/licenses/gpl-3.0.html.
"""
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

	# redirect domains without specific rules
	if domain in roadmap:
		return roadmap[domain]
	return roadmap["rest"]

open_with = roadmap_url(domain)

# and just start binary with flags!:)
print(f"Launch Options: {str(open_with+[url])}") # +unknown (?)
with subprocess.Popen(open_with+[url]) as _:
	pass
