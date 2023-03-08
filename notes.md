# Interview at GI w/ Josh

https://codeshare.io/QnEklJ
test: https://codeshare.io/N3pmYJ

https://onecompiler.com/python/3yytb9brs


ls = [2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18]



def CrawlIntervals(ls, cost_d, interval, maxinterval):
  if not 1 <= interval <= maxinterval:
    return None

  mincost = InnerLoop(interval, ls, maxinterval)
  cost_d[interval] = mincost

  if interval + 1 not in cost_d:
    CrawlIntervals(ls, cost_d, interval + 1, maxinterval)
  if interval - 1 not in cost_d:
    CrawlIntervals(ls, cost_d, interval - 1, maxinterval)

  return None




def SearchIntervals(ls, cost_d, leftinterval, rightinterval, maxinterval):
  if rightinterval <= leftinterval:
    return None

  mid = (rightinterval + leftinterval) // 2
  current_cost = InnerLoop(mid, ls, maxinterval)
  # print('leftinterval, rightinterval:', leftinterval, rightinterval)
  # print('interval, current_cost:', mid, current_cost)
  cost_d[mid] = current_cost

  if mid + 1 not in cost_d:
    SearchIntervals(ls, cost_d, mid + 1, rightinterval, maxinterval)
  if mid - 1 not in cost_d:
    SearchIntervals(ls, cost_d, leftinterval, mid, maxinterval)
  return None
