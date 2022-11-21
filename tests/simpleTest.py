import unittest

class TestAdd(unittest.TestCase):

  def test_add (self):
    self.assertEqual(1 + 2, 3)
  
  
  
if __name__ == '__main__':  
    unittest.main()
    