import unittest, os, sys
import codecs

module_location = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.dirname(module_location)))

from pytvrename import *

class TestAgainstFile(unittest.TestCase):
	
	def setUp(self):
		"""load the file"""
		filename = module_location + "/" + "showList.txt"
		self.file = open( filename, "r" )
	
	def tearDown(self):
		"""close the file"""
		self.file.close()


	def testOneShow(self):
		"""tests whether the name of """
		# for line in self.file:
		# 	print line
		line = self.file.readline()
		info = scrapeFilename( line )
		assert info['show'] == "Chuck"
		
	def testRenameFile(self):
		""" """
		for line in self.file:
			info = scrapeFilename( line )
			info['show'] = normalizeShowName( info['show'] )
			info['season'] = int( info['season'] )
			info['episode'] = int( info['episode'] )
			name = getEpisodeName( info['show'], info['season'], info['episode'])
			print line
			print generateCorrectFilename( info['show'], info['season'], info['episode'], name)


class TestRenaming(unittest.TestCase):
	"""docstring for TestRenaming"""
	def setUp(self):
		"""load the file"""
		print "open"
		self.file = codecs.open( "showList.txt", "r" )

	def tearDown(self):
		"""close the file"""
		print "close"
		self.file.close()
	
	def testRenaming(self):
		"""docstring for test"""
		print "testRenaming"
		for line in self.file:
			try:
				info = scrapeFilename( line )
				print line + " -> " + str(info)
			except:
				print line

		
	
class TestEpisodeGuide(unittest.TestCase):
	"""docstring for TestEpisodeGuide"""

	def setUp(self):
		""" specify a set of known cases """
		self.testCases = [
			{
				'show': "House",
				'episode': 11,
				'season': 3,
				'title': "Words and Deeds"
			},
			{
				'show': "Lost",
				'episode': 21,
				'season': 2,
				'title': "?"
			},
			{
				'show': "Heroes",
				'episode': 15,
				'season': 1,
				'title': "Run!"
			}
		]
	
	# 
	def testGetEpisodeName(self):
		""" test the episode name of each of the cases """
		for case in self.testCases:
			assert case['title'] == getEpisodeName( case['show'], case['season'], case['episode'])
	



if __name__ == "__main__":
      unittest.main()   
