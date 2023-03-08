import math
import random
import sys

ITERS = 0


def FindMaxInterval(ls):
  """Find the maximum interval of the given list of integers.

  When the elements are all equal, the return value should == 1.
  """
  m = 1
  i = 0
  j = 1
  while j < len(ls):
    interval = ls[j] - ls[i]
    m = max(m, interval)
    i += 1
    j += 1
    global ITERS
    ITERS += 1
  return m


def GetMinimumCost(ls, interval, maxinterval):
  """Return the minimum cost to produce an equidistant list with the given
  interval.
  """
  cost_list = []

  # The maximum steps which the head of this list may have to move, before the
  # interval sequence begins, should be within range(-maxinterval,
  # maxinterval+1).

  # we arbitrarily choose the leftmost element as an anchor.
  for leftmost_offset in range(-maxinterval, maxinterval + 1):
    total_cost = 0
    leftmost_pos = ls[0] + leftmost_offset

    for j, abs_pos in enumerate(ls):
      future_pos = leftmost_pos + (j * interval)
      delta = abs(abs_pos - future_pos)
      total_cost += delta
      global ITERS
      ITERS += 1
    cost_list.append(total_cost)

  return min(cost_list)


def GetPreviousCost(cost_d, default_interval):
  """Retrieve the recorded cost of a previous run.
  """

  if cost_d:
    previous_int, previous_cost = list(cost_d.items())[-1]
  else:
    previous_int, previous_cost = default_interval, sys.maxsize
  return previous_int, previous_cost


def CrawlIntervals(ls, cost_d, interval, maxinterval):
  """Recursive crawler, looking for minimum cost.
  """

  if not 1 <= interval <= maxinterval:
    return None

  current_cost = GetMinimumCost(ls, interval, maxinterval)
  previous_int, previous_cost = GetPreviousCost(cost_d, interval)
  cost_d[interval] = current_cost

  if current_cost < previous_cost:
    if interval + 1 not in cost_d:
      CrawlIntervals(ls, cost_d, interval + 1, maxinterval)
    if interval - 1 not in cost_d:
      CrawlIntervals(ls, cost_d, interval - 1, maxinterval)

  return None


def SearchIntervals(ls, cost_d, leftinterval, rightinterval, maxinterval):
  """Recursive binary search, looking for minimum cost.
  """

  mid = (rightinterval + leftinterval) // 2
  if leftinterval >= rightinterval or mid in cost_d:
    return None
  current_cost = GetMinimumCost(ls, mid, maxinterval)

  previous_int, previous_cost = GetPreviousCost(cost_d, mid)
  cost_d[mid] = current_cost

  if current_cost < previous_cost:
    # we allow mid == previous_int, so that the first run checks both
    # directions.
    if mid <= previous_int:
      SearchIntervals(ls, cost_d, leftinterval, mid, maxinterval)

    if mid >= previous_int:
      SearchIntervals(ls, cost_d, mid + 1, rightinterval, maxinterval)

  # Go back to where we were, and look around. This seems to have minimal cost:
  else:
    # we turned left
    if previous_int == rightinterval:
      SearchIntervals(ls, cost_d, mid, previous_int, maxinterval)
    # we turned right
    elif previous_int == leftinterval + 1:
      SearchIntervals(ls, cost_d, previous_int, mid, maxinterval)

  return None


def LikeliestBigO(iters, size, maxinterval):
  """Gives a rough idea of O() complexity.

  Note: in the stricter sense, we should only return the positive delta.
  """

  runtimes = {
      'logn_delta': abs(iters - math.log(size, 2)),
      'linear_delta': abs(iters - size),
      'length^2_delta': abs(iters - size**2),
      'length^3_delta': abs(iters - size**3),
      'maxinterval^2_delta': abs(iters - maxinterval**2),
      'maxinterval^3_delta': abs(iters - maxinterval**3),
      '(maxinterval*size)^2_delta': abs(iters - (maxinterval * size)**2),
      '(maxinterval*size)^3_delta': abs(iters - (maxinterval * size)**3),
  }
  return min(runtimes.items(), key=lambda x: x[1])


def RunExperiments(maxdistance=100, maxnum=50, maxexperiments=20):
  """Run experiments produced by random.randint().
  """

  random.seed()
  experiments = [[
      random.randint(1, maxdistance) for _ in range(random.randint(2, maxnum))
  ] for _ in range(maxexperiments)]
  # we take the liberty of a presorted list:
  experiments = [sorted(ls) for ls in experiments]

  results = {}
  for exp in experiments:
    global ITERS
    ITERS = 0
    search_cost_d = {}
    leftinterval = 1
    maxinterval = FindMaxInterval(exp)
    begin = maxinterval // 2
    CrawlIntervals(exp, search_cost_d, begin, maxinterval)
    try:
      minimum = min(search_cost_d.items(), key=lambda x: x[1])
    except:
      print(search_cost_d, exp)

    results[tuple(exp)] = (minimum, maxinterval, ITERS)
  return results


if __name__ == '__main__':
  ls = [2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18]

  maxinterval = FindMaxInterval(ls)
  print('maxinterval:', maxinterval)

  search_cost_d = {}
  leftinterval = 1
  # note: we pass maxinterval+1 as the rightinterval, to include it in the
  # search space.
  SearchIntervals(ls, search_cost_d, leftinterval, maxinterval + 1,
                  maxinterval)
  minimum = min(search_cost_d.items(), key=lambda x: x[1])
  print('search_cost_d:', search_cost_d)
  print('minimum:', minimum)

  crawl_cost_d = {}
  # we start the crawler at the midpoint, but any point is possible.
  begin = maxinterval // 2
  CrawlIntervals(ls, crawl_cost_d, begin, maxinterval)
  minimum = min(crawl_cost_d.items(), key=lambda x: x[1])
  print('crawl_cost_d:', crawl_cost_d)
  print('minimum:', minimum)

  # Run experiments on CrawlIntervals:
  # We're well past O(n^2), as long as the length of the list is considered n.
  # As it is, it's the maximum interval that makes this so expensive.
  # O(maxinterval^3) is more likely.
  results = RunExperiments()
  for exp, ((interval, cost), maxinterval, iters) in results.items():
    print('\nExperiment:')
    print(f'length: {len(exp)}; final interval: {interval}; '
          f'cost: {cost}; maxinterval: {maxinterval}; iterations: {iters}')
    print('Likliest runtime complexity:',
          LikeliestBigO(iters, len(exp), maxinterval))
