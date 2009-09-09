import unittest
import pytvrename


class TestAgainstFile(unittest.TestCase):
	
	def setUp(self):
		"""load the file"""
		self.file = open( "untitled.txt", "r" )
	
	def tearDown(self):
		"""close the file"""
		self.file.close()


	def testShow(self):
		"""tests whether the name of """
		# for line in self.file:
		# 	print line
		line = self.file.readline()
		info = pytvrename.scrapeFilename( line )
		print info['show']
		assert info['show'] == "Chuck"
		
	
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
			assert case['title'] == pytvrename.getEpisodeName( case['show'], case['season'], case['episode'])
	
		
	# def testSeason(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2
	# 	
	# def testEpisodeName(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2

if __name__ == "__main__":
      unittest.main()   
