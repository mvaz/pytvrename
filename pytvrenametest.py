import unittest
import pytvrename


class TestAgainstFile(unittest.TestCase):
	
	def setUp(self):
		"""load the file"""
		self.file = open( "fullShowList.txt", "r" )
	
	def tearDown(self):
		"""close the file"""
		self.file.close()


	def testShow(self):
		"""tests whether the name of """
		# for line in self.file:
		# 	print line
		assert 2 == 2
	
class TestEpisodeGuide(unittest.TestCase):
	"""docstring for TestEpisodeGuide"""

	def setUp(self):
		""" """
		self.show = "House"
		self.episode = 11
		self.season = 3
		self.title  = "Words and Deeds"
		
	def testGetEpisodeName(self):
		""" """
		assert self.title == pytvrename.getEpisodeName( self.show, self.season, self.episode)
	
		
		
	# def testSeason(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2
	# 	
	# def testEpisodeName(self):
	# 	"""tests whether the name of """
	# 	assert 1 == 2

if __name__ == "__main__":
      unittest.main()   
