#!/usr/bin/python

import os
import re

from pytvrename import *


TEST_DIR = os.path.join( os.path.abspath(os.path.dirname(__file__)), "test", "testdirectory")
TORRENTS_DIR = os.path.join( TEST_DIR, "torrentsdir")
MOVIE_DIR    = os.path.join( TEST_DIR, "moviedir")

# class Show:
#     def __init__(self, title="", rating=0):
#         self.title = title
#         self.attributes = {}
#         self.episodes = {}
# 
# class ShowRenamer:
# 	


def isMovieFile(filename):
	"""
	determines whether a given file is a movie file 
	currently give by a simple regular expression
	TODO add isfile test
	"""
	reg = re.compile( ".*?.avi$", re.I | re.U )
	return reg.match(filename)

	
def main():
	"""docstring for main"""
	# sl = ShowList()
	# sl.updateListEZTV()

	# print getEpisodeName( "Chuck", 2, 1)

	# list the directory
	dirList = os.listdir(TORRENTS_DIR)
	for file in dirList:
		if not isMovieFile( file ):
			continue
		zbr = scrapeFilename( file )
		print zbr['show'], int(zbr['season']), int(zbr['episode'] )
		# print zbr['show'], zbr['episode'], zbr['season']
		print getEpisodeName( zbr['show'], int(zbr['season']), int(zbr['episode'] ) )
	
	
	
	
if __name__ == "__main__":
    main()


# base_path = '/SlugMedia/Videos/TV'
# 
# for show in os.listdir( base_path ):
#     show_path = os.path.join( base_path, show )
#     if not os.path.isdir( show_path ):
#         continue
# 
#     expression = show + "\s*-\s*(?:Season|Series)\s*(\d)"
#     pattern = re.compile( expression )
# 
#     for season in os.listdir( show_path ):
#         m = re.match( pattern, season, re.IGNORECASE )
#         if m:
#             number = m.group(1)
#             old = os.path.join( show_path, season )
#             new = os.path.join( show_path, "Season " + number )
#             #print old + " -> " + new
#             os.rename( old, new )
