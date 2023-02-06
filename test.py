import unittest


class TestModule(unittest.TestCase):
  def setUp(self):
    pass

  def testEmpty(self):
    self.assertEqual(None, None)

if __name__ == '__main__':
  unittest.main()
