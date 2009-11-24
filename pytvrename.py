#!/usr/bin/env python
# encoding: utf-8
"""
pytvrename.py

Created by Miguel Vaz on 2009-08-31.
Copyright (c) 2009. All rights reserved.
"""

import sys, os
import urllib2, re
import difflib
from BeautifulSoup import BeautifulSoup, SoupStrainer


class EpisodeRenamer(object):
	"""
	docstring for EpisodeRenamer
	"""
	
	def __init__(self):
		super(EpisodeRenamer, self).__init__()
		self.showCache = dict()
		self.list = []
	
	@staticmethod
	def normalizeShowTitleEZTV( showTitle ):
		""" 
		removes 
		"""
		cleanShowTitle = re.sub( r'[\,\.\'\;\"\ ]', '', showTitle)
		cleanShowTitle = re.sub( r'^The', '', cleanShowTitle, re.I)
		return cleanShowTitle
	
	
	@staticmethod
	def getPageOfShowFromEZTV( show ):
		""" 
		Reads the epguides.com page of the show and returns the html contents 
		"""
		url = "http://epguides.com/%s" % (show)
		response = urllib2.urlopen(url)
		html = response.read()
		html = html.decode('iso-8859-1')
		return html
	
	
	def __updateShowListEZTV(self):
		""" updates the list of tvshows from the eztv website """
		showListURL = "http://ezrss.it/shows/"
		html = urllib2.urlopen( showListURL ).read()
		links = SoupStrainer('a', href=re.compile('show_name') )
		self.list = [ tag.contents[0] for tag in BeautifulSoup(html, parseOnlyThese=links)]
	
	
	def normalizeShowTitle(self, title):
		""" takes a string containing a title, and returns the most probable from the list """
		if self.list == []:
			self.__updateShowListEZTV()
		zbr = difflib.get_close_matches( title, self.list, n=1 )
		return zbr[0]
	
	
	def getPageOfShow( self, show ):
		""" 
		Reads the epguides.com page of the show and returns the html contents 
		"""
		show = EpisodeRenamer.normalizeShowTitleEZTV( show )
		if not show in self.showCache:
			try:
				self.showCache['show'] = EpisodeRenamer.getPageOfShowFromEZTV( show )
			except:
				raise ShowNotFoundError("show name '%s' not recognized by eztv" % (show) )
		
		return self.showCache['show']


	def getShowList( self ):
		"""docstring for getShowList"""
		showListURL = "http://ezrss.it/shows/"
		# download page
		html = urllib2.urlopen( showListURL ).read()
		
		links = SoupStrainer('a', href=re.compile('show_name') )
		liste = [ tag.contents[0] for tag in BeautifulSoup(html, parseOnlyThese=links)]
		
		return liste
	
	
	def getEpisodeName( self, episode ):
		""" 
		Reads the epguides.com page of the show
		and returns the title of a given episode and season
		"""
		
		# 
		page = self.getPageOfShow( episode.show )
    
	    # remove <script> stuff, because it breaks BeautifulSoup
		p = re.compile('<div\s*id=\"(footer)\".*?<\/div>', re.IGNORECASE | re.DOTALL | re.U) 
		html = p.sub( "", page)
		# parse the page
		soup = BeautifulSoup(html)
		# find the part that has the episode list
		page = soup.find(id="eplist").pre
    
		# compile the regular expression
		reg = "^\s*\d+\.?\s+%(season)d-\s*(?:%(number)2d|%(number)02d)\s*[\w\d\/]{3,}\s*(.*$)" % {'season': int(episode.season), 'number': int(episode.number) }
		reg = re.compile( reg, re.I | re.U )
		
		reg2 = re.compile( "<a.*?>([^<\"]*)<\/a>\s*$", re.I )
		    
		# split the page into different lines
		for line in str(page).splitlines():
			if reg.search( line ):
				title = reg2.search( line ).group(1)
				break
		else:
			# TODO raise EpisodeNotFound exception
			raise EpisodeNotFound("Episode %d, of season %d, of show %s not found" % (episode.number, episode.season, episode.show) )
    
		return title
	

class ShowNotFoundError(Exception):
	""" docstring for EpisodeNotFound """
	def __init__(self,value):
		self.value = value
	
	def __str__(self):
		return str(self.value)
	



class EpisodeNotFound(Exception):
	""" docstring for EpisodeNotFound """
	def __init__(self, value):
		super(EpisodeNotFound, self).__init__()
		self.value = value
	
	def __str__(self):
		return str(self.value)




class Show(object):
	""" holds the info for a TVShow """
	def __init__(self, name):
		super(Show, self).__init__()
		self.name = name
		

class Episode(object):
	""" holds the information for an episode """
	def __init__(self, show, season, episode, title = ""):
		super(Episode, self).__init__()
		self.show = show
		self.season = int(season)
		self.number = int(episode)
		self.title = title
	
	@staticmethod
	def createEpisodeFromFilename( filename ):
		""" """
		reg = "(?P<path>.*\/)?(?P<show>.*?)[\._\ \-]+?[Ss]?(?P<season>\d+)[\._ \-]?[EeXx]?(?P<number>\d+)[\._ \-]"
		reg = re.compile( reg, re.I | re.U )
		zbr = reg.search( filename )
		return Episode( zbr.group('show'), zbr.group('season'), zbr.group('number'), "" )
	
	
	def generateCorrectFilename(self, pattern = "%s S%02dE%02d %s.avi"):
		""" """
		return pattern % (self.show, self.season, self.number, self.title)
	

	

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