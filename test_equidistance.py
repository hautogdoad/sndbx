import equidistance

import unittest


class TestBinSearch(unittest.TestCase):

  def setUp(self):
    self.search_cost_d = {}
    self.default_leftinterval = 1

  def testNoMoves(self):
    ls = [0, 1, 2]
    maxinterval = equidistance.FindMaxInterval(ls)
    equidistance.SearchIntervals(ls, self.search_cost_d,
                                 self.default_leftinterval, maxinterval + 1,
                                 maxinterval)
    minimum = min(self.search_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (1, 0))

  def testStacked(self):
    ls = [3, 3, 3]
    maxinterval = equidistance.FindMaxInterval(ls)
    equidistance.SearchIntervals(ls, self.search_cost_d,
                                 self.default_leftinterval, maxinterval + 1,
                                 maxinterval)
    minimum = min(self.search_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (1, 2))

  def testBigInitialInterval(self):
    ls = [0, 45, 46, 47]
    maxinterval = equidistance.FindMaxInterval(ls)
    equidistance.SearchIntervals(ls, self.search_cost_d,
                                 self.default_leftinterval, maxinterval + 1,
                                 maxinterval)
    minimum = min(self.search_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (23, 44))
    self.assertEqual(self.search_cost_d, {12: 44, 17: 44, 23: 44, 35: 92})

  def testBigInitialAndEndInterval(self):
    ls = [0, 45, 46, 47, 92]
    maxinterval = equidistance.FindMaxInterval(ls)
    equidistance.SearchIntervals(ls, self.search_cost_d,
                                 self.default_leftinterval, maxinterval + 1,
                                 maxinterval)
    minimum = min(self.search_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (23, 44))
    self.assertEqual(self.search_cost_d, {
        12: 66,
        17: 56,
        20: 50,
        22: 46,
        23: 44,
        35: 116
    })

  def testBigRandomList(self):
    ls = [
        51, 96, 106, 148, 151, 184, 187, 207, 240, 257, 273, 276, 289, 297,
        299, 313, 335, 352, 361, 389, 394, 412, 415, 482, 489, 539, 560, 659,
        684, 692, 717, 736, 779, 808, 814, 818, 836, 847, 861, 870, 883, 894,
        915, 917, 919, 937, 944, 955, 957, 989
    ]
    maxinterval = equidistance.FindMaxInterval(ls)
    equidistance.SearchIntervals(ls, self.search_cost_d,
                                 self.default_leftinterval, maxinterval + 1,
                                 maxinterval)
    minimum = min(self.search_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (19, 1950))

    # fails to find this better alternative:
    better = equidistance.GetMinimumCost(ls, 20, maxinterval)
    self.assertEqual(better, 1879)


class TestCrawler(unittest.TestCase):

  def setUp(self):
    self.crawl_cost_d = {}

  def testNoMoves(self):
    ls = [0, 1, 2]
    maxinterval = equidistance.FindMaxInterval(ls)
    begin = max(1, maxinterval // 2)
    equidistance.CrawlIntervals(ls, self.crawl_cost_d, begin, maxinterval)
    minimum = min(self.crawl_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (1, 0))

  def testStacked(self):
    ls = [3, 3, 3]
    maxinterval = equidistance.FindMaxInterval(ls)
    begin = max(1, maxinterval // 2)
    equidistance.CrawlIntervals(ls, self.crawl_cost_d, begin, maxinterval)
    minimum = min(self.crawl_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (1, 2))

  def testBigInitialInterval(self):
    ls = [0, 45, 46, 47]
    maxinterval = equidistance.FindMaxInterval(ls)
    begin = max(1, maxinterval // 2)
    equidistance.CrawlIntervals(ls, self.crawl_cost_d, begin, maxinterval)
    minimum = min(self.crawl_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (22, 44))

  def testBigInitialAndEndInterval(self):
    ls = [0, 45, 46, 47, 92]
    maxinterval = equidistance.FindMaxInterval(ls)
    begin = max(1, maxinterval // 2)
    equidistance.CrawlIntervals(ls, self.crawl_cost_d, begin, maxinterval)
    minimum = min(self.crawl_cost_d.items(), key=lambda x: x[1])
    self.assertEqual(minimum, (23, 44))

  def testBigRandomList(self):
    ls = [
        51, 96, 106, 148, 151, 184, 187, 207, 240, 257, 273, 276, 289, 297,
        299, 313, 335, 352, 361, 389, 394, 412, 415, 482, 489, 539, 560, 659,
        684, 692, 717, 736, 779, 808, 814, 818, 836, 847, 861, 870, 883, 894,
        915, 917, 919, 937, 944, 955, 957, 989
    ]
    maxinterval = equidistance.FindMaxInterval(ls)
    begin = max(1, maxinterval // 2)
    equidistance.CrawlIntervals(ls, self.crawl_cost_d, begin, maxinterval)
    minimum = min(self.crawl_cost_d.items(), key=lambda x: x[1])

    self.assertEqual(minimum, (20, 1879))

    # nearby alternatives aren't better:
    res = equidistance.GetMinimumCost(ls, 19, maxinterval)
    self.assertTrue(res > minimum[1])

    res = equidistance.GetMinimumCost(ls, 18, maxinterval)
    self.assertTrue(res > minimum[1])

    res = equidistance.GetMinimumCost(ls, 21, maxinterval)
    self.assertTrue(res > minimum[1])


if __name__ == '__main__':
  unittest.main()
