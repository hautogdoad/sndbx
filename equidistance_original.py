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


def SearchIntervals(ls, cost_d, leftinterval, rightinterval, maxinterval):
  """Recursively search [leftinterval, rightinterval), looking for minimum cost.
  """

  if leftinterval >= rightinterval:
    return None

  mid = (rightinterval + leftinterval) // 2
  current_cost = GetMinimumCost(mid, ls, maxinterval)

  if cost_d:
    previous_int, previous_cost = list(cost_d.items())[-1]
  else:
    # allowing for the first run:
    previous_int, previous_cost = mid, sys.maxsize

  cost_d[mid] = current_cost

  if current_cost < previous_cost:
    # we allow mid == previous_int, so that the first run checks both
    # directions.
    if mid <= previous_int:
      SearchIntervals(ls, cost_d, leftinterval, mid, maxinterval)

    if mid >= previous_int:
      SearchIntervals(ls, cost_d, mid + 1, rightinterval, maxinterval)

  return None


def GetMinimumCost(interval, ls, maxinterval):
  """Return the minimum cost to produce an equidistant list with the given
  interval.
  """

  # maximum steps which the head or tail of this list may have to move, before
  # the interval sequence matching the minimum cost begins.
  # FIXME: still unclear whether this scope is really necessary.
  # maxmove = len(ls) * maxinterval
  # maxmove = maxinterval + 1
  minmove = sys.maxsize

  cost_list = []
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

    if total_cost < minmove:
      minmove = total_cost
      print('leftmost_pos:', leftmost_pos, minmove, interval)

    cost_list.append(total_cost)

  return min(cost_list)


def LikeliestBigO(iters, size, maxinterval):
  runtimes = {
      'logn_delta': abs(iters - math.log(size, 2)),
      'linear_delta': abs(iters - size),
      'length^2_delta': abs(iters - size**2),
      'length^3_delta': abs(iters - size**3),
      'maxinterval^2_delta': abs(iters - maxinterval**2),
      'maxinterval^3_delta': abs(iters - maxinterval**3),
      '(maxinterval*size)^2_delta': abs(iters - (maxinterval*size)**2),
      '(maxinterval*size)^3_delta': abs(iters - (maxinterval*size)**3),
  }
  return min(runtimes.items(), key=lambda x: x[1])


def RunExperiments(maxdistance=20, maxnum=50, maxexperiments=20):
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
    SearchIntervals(exp, search_cost_d, leftinterval, maxinterval + 1,
                    maxinterval)
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


  # We're well past O(n^2), as long as the length of the list is considered n.
  # As it is, it's the maximum interval that makes this so expensive.
  # O((maxinterval*length)^2) is more likely.

  # results = RunExperiments()
  # for exp, ((interval, cost), maxinterval, iters) in results.items():
  #   print('\nExperiment:')
  #   print(
  #     f'length: {len(exp)}; final interval: {interval}; '
  #     f'cost: {cost}; maxinterval: {maxinterval}; iterations: {iters}'
  #   )
  #   print('Likliest runtime complexity:', LikeliestBigO(iters, len(exp), maxinterval))
