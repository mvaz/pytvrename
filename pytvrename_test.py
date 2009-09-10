import unittest
from pytvrename import *


class TestAgainstFile(unittest.TestCase):
	
	def setUp(self):
		"""load the file"""
		self.file = open( "untitled.txt", "r" )
	
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
			}
		]
		
	
	def testGetEpisodeName(self):
		""" test the episode name of each of the cases """
		for case in self.testCases:
			assert case['title'] == getEpisodeName( case['show'], case['season'], case['episode'])
	
		
	# def testSeason(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2
	# 	
	# def testEpisodeName(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2

if __name__ == "__main__":
      unittest.main()   
