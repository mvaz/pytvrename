#!/usr/bin/python

import os
import re

from pytvrename import *

# class Show:
#     def __init__(self, title="", rating=0):
#         self.title = title
#         self.attributes = {}
#         self.episodes = {}
# 
# class ShowRenamer:
# 	
	
	
def main():
	"""docstring for main"""
	sl = ShowList()
	sl.updateListEZTV()
	print sl.list
	
	
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
