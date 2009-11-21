#!/usr/bin/env python
# encoding: utf-8
"""
pytvrename.py

Created by Miguel Vaz on 2009-08-31.
Copyright (c) 2009. All rights reserved.
"""

import sys, os
import urllib2, re
from BeautifulSoup import BeautifulSoup, SoupStrainer


def getPageOfShow( show ):
	""" 
	Reads the epguides.com page of the show and returns the html contents 
	"""
	url = "http://epguides.com/" + show
	response = urllib2.urlopen(url)
	html = response.read()
	html = html.decode('iso-8859-1')
	return html


def getShowList( ):
	"""docstring for getShowList"""
	showListURL = "http://ezrss.it/shows/"
	# download page
	html = urllib2.urlopen( showListURL ).read()
	
	links = SoupStrainer('a', href=re.compile('show_name') )
	liste = [ tag.contents[0] for tag in BeautifulSoup(html, parseOnlyThese=links)]
	
	return liste

class Show(object):
	"""
	"""


class ShowList(object):
	"""
	docstring for ShowList
	"""
	FILE, EZTV, PYTVSHOWS = range(3)
    	
	def __init__(self, mode = EZTV, list = []):
		self.mode = mode
		self.list = list
	
	def updateListEZTV(self):
		""" docstring for fillList """
		showListURL = "http://ezrss.it/shows/"
		
		html = urllib2.urlopen( showListURL ).read()
		links = SoupStrainer('a', href=re.compile('show_name') )
		self.list = [ tag.contents[0] for tag in BeautifulSoup(html, parseOnlyThese=links)]
		
	def normalizeShowTitle(self, title):
		""" takes a string containing a title, and returns the most probable from the list """
		# [\.\']
		return title
	
	


def getEpisodeName( show, season, episode ):
	""" 
	Reads the epguides.com page of the show
	and returns the title of a given episode and season
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
	reg = "\s*\d+\.?\s+%(season)s-\s*(?:%(episode)2d|%(episode)02d)\s*[\w\d]{3,}\s*(.*$)" % {'season': str(season), 'episode': int(episode) }
	reg = re.compile( reg, re.I | re.U )
	
	reg2 = re.compile( "<a.*?>([^<\"]*)<\/a>\s*$", re.I )
	
	# split the page into different lines
	for line in str(page).splitlines():
		if reg.search( line ):
			title = reg2.search( line ).group(1)
			break
	else:
		# TODO raise EpisodeNotFound exception
		print "nothing found"
		title = ""
	
	return title



def scrapeFilename( filename ):
	""" takes the filename and returns the show, episode and season """
	reg = "(?P<path>.*\/)?(?P<show>.*?)[\._\ \-]+?[Ss]?(?P<season>\d+)[\._ \-]?[EeXx]?(?P<episode>\d+)[\._ \-]"
	reg = re.compile( reg, re.I | re.U )
	result = reg.search( filename )
	return result.groupdict()


def normalizeShowName( show ):
	""" several possibilities for this:
	  - list + levenshtein
	  - guess it from epguides
	"""
	show = re.sub( r'#.*$', "", show)
	return show
	# 1 regularize filename




def generateCorrectFilename( show, season, episode, title ):
	# return "%s S%dE%d %s" % [ show, season, episode, title ]
	return show + "-" + str(season) + str(episode) + title


def finalPath( baseDir, show, season, fileName):
	return "%s/%s/Season %s/%s" % [ baseDir, show, season, fileName ]




def levenshtein(s1, s2):
	if len(s1) < len(s2):
		return levenshtein(s2, s1)
	if not s1:
		return len(s2)
	
	previous_row = xrange(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
		
	return previous_row[-1]

# def lev(a, b):
# 	if not a: return len(b)
# 	if not b: return len(a)
# 	return min(lev(a[1:], b[1:])+(a[0] != b[0]), lev(a[1:], b)+1, lev(a, b[1:])+1)


# 
# def main():
# 	# show = "Lost"
# 	# 	title = getEpisodeName( show, 3, 11)
# 	sl = ShowList()
# 	sl.updateListEZTV()
# 	print sl.list
# 	# soup = BeautifulSoup( html )
# 	# zbr = soup.findAll( )
# 	# linksToBob = SoupStrainer('a', href=re.compile('bob.com/'))
# 	# print levenshtein( "saa", "sab")
# 
# 
# if __name__ == '__main__':
# 	main()

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