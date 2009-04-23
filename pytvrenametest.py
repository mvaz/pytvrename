import unittest
import pytvrename


class TestAgainstFile(unittest.TestCase):
	
	def setUp(self):
		"""load the file"""
		self.file = open( "showList.txt", "r" )
	
	def tearDown(self):
		"""close the file"""
		self.file.close()


	def testShow(self):
		"""tests whether the name of """
		assert 1 == 2
		
	def testSeason(self):
		"""tests whether the name of """
		assert 1 == 2
		
	def testEpisodeName(self):
		"""tests whether the name of """
		assert 1 == 2

if __name__ == "__main__":
      unittest.main()   
