#!/usr/bin/env python
# encoding: utf-8
"""
pytvrename.py

Created by Miguel Vaz on 2009-08-31.
Copyright (c) 2009. All rights reserved.
"""

import sys, os
import urllib2, re
from BeautifulSoup import BeautifulSoup


def getPageOfShow( show ):
	""" 
	Reads the epguides.com page of the show and returns the html contents 
	"""
	url = "http://epguides.com/" + show
	response = urllib2.urlopen(url)
	html = response.read()
	html = html.decode('iso-8859-1')
	return html


def getEpisodeName( show, season, episode ):
	""" 
	"""
	page = getPageOfShow( show )

    # remove <script> stuff, because it breaks BeautifulSoup
	p = re.compile('<div\s*id=\"(footer)\".*?<\/div>', re.IGNORECASE | re.DOTALL | re.U) 
	html = p.sub( "", page)
	# parse the page
	soup = BeautifulSoup(html)
	# find the part that has the episode list
	page = soup.find(id="eplist").pre

	# compile the regular expression
	reg = "\s*\d+\.\s+%(season)s-\s*%(episode)s.*? \w{3} \d{2}(.*$)" % {'season': str(season), 'episode': str(episode)}
	reg = re.compile( reg, re.I | re.U )
	
	reg2 = re.compile( "<a.*?>(.*?)<\/a>", re.I )

	# split the page into different lines
	for line in str(page).splitlines():
		if reg.search( line ):
			title = reg2.search( line ).group(1)
			break
	else:
		# TODO raise EpisodeNotFound exception
		title = ""

	return title


def scrapeFilename( filename ):
	return { "show": "Show", "season": 1, "episode": 1}

def finalPath( baseDir, show, season, fileName):
	return "%s/%s/Season %s/%s" % [ baseDir, show, season, fileName ]

def main():
	show = "House"
	title = getEpisodeName( show, 3, 11)
	print title


if __name__ == '__main__':
	main()




	#case Format_EpGuides { #{{{
	# EpGuides.com format
	#                            Original
	#  Episode #      Prod #     Air Date   Episode Title
	#_____ ______ ____________ ___________ ___________________________________________
	#
	#
	#Season 1
	#
	#  1.   1- 1                26 Mar 05   Rose
	#  2.   1- 2                 2 Apr 05   The End of the World
	#  3.   1- 3                 9 Apr 05   The Unquiet Dead
	##
	# OR (after simplification that takes place prior to this stage)
	##
	#  1.   1- 1                26 Mar 05   <a>Rose</a>
	#  2.   1- 2                 2 Apr 05   <a>The End of the World</a>
	#  3.   1- 3                 9 Apr 05   <a>The Unquiet Dead</a>
	#
	# NB: The air date is missing in some cases
	#
	# 	my ($num, $epTitle);
	# 	
	# 	foreach(@input)
	# 	{
	# 		# Most episodes
	# 		if( ($num, $epTitle) = ($_ =~ /\s*\d+\.\s+$season-(..).*? \w{3} \d{2}(.*$)/) )
	# 		{
	# 			# Cleanup whitespace (and tags if using online version)
	# 			($epTitle) = ($epTitle =~ /^\s*(?:\<a\>)?(.*?)(?:\<\/a\>)?$/);
	# 			check_and_push($epTitle, \@name, $num);
	# 		}
	# 		# Pilot episodes (c.f. "Lost" & "24" season 1)
	# 		elsif( ($num, $epTitle) = ($_ =~ /\s+P-\s*(\d+).*?\d+ \w{3} \d{2}(.*$)/) )
	# 		{
	# 			# Cleanup whitespace (and tags if using online version)
	# 			($epTitle) = ($epTitle =~ /^\s*(?:\<a\>)?(.*?)(?:\<\/a\>)?$/);
	# 			check_and_push($epTitle, \@pname, $num);
	# 		}
	# 	}
	# 
	# } # End Format_EpGuides }}}