#! /usr/bin/python

import random
from datetime import datetime, date, time
import itertools
import operator
import bisect

global maxPerBucket, debug
maxPerBucket = 5  # Max number of beans per bucket. try larger numbers for fun
debug = False  # Control verbose print

random.seed(datetime.now())

def main() :
  while True :  # Loop to try data points non-stop
    data = MakeData()
    buckets = data["buckets"]
    redBeans = data["redBeans"]
    chests = [[0 for i in xrange(5)] for j in xrange(20)]
    collisionDistance = 20  # Number of shuffles to see a collision
    nBucketsOnSplitLevel = 0

    for redBean in redBeans :  # Red beans go to the bottom drawers
      chests[redBeans.index(redBean)][0] = redBean

    # Drop beans by buckets into the drawers on the same level.
    # Go to the beginning of the higher level when the current level is full.
    chestIdx = 0
    drawerIdx = 1
    for bucket in buckets :
      start = [chestIdx, drawerIdx]  # Start position of the current bucket
      for beanID in bucket :
        if beanID % 2 == 0 :  # Skip red beans
          chests[chestIdx][drawerIdx] = beanID
          drawerIdx += 1 if chestIdx + 1 == 20 else 0
          chestIdx = (chestIdx + 1) % 20

      end = [chestIdx, drawerIdx]  # Finish position
      if start[1] != end[1] and end[0] > 0 :  # Beans are on two levels
        nBucketsOnSplitLevel += 1
        distance = start[0] - end[0]
        collisionDistance = min(collisionDistance, distance)
        firstBean = chests[0][drawerIdx]
        if debug: print "2-level", distance, start, end, bucket, firstBean
    # end of outer for loop

    CheckResult(chests, False)  # Don't expect collision

    # Shuffle by shifting the drawers on the same level, so that a bean will
    # not see its previous "chest-mates" any more.
    # Shuffle only when collisions are possible and stop when a collision is
    # first observed (when collisionDistance is covered).
    if collisionDistance < 20 :
      for move in range(0, collisionDistance + 1) :
        newChests = [[0 for i in xrange(5)] for j in xrange(20)]
        # Shift the drawers. The bottom drawers don't move.
        # Higher levels shift incrementally more.
        for drawerIdx in range(0, 5) :
          for chestIdx in range(0, 20) :
            targetChestIdx = (chestIdx + drawerIdx) % 20
            newChests[targetChestIdx][drawerIdx] = chests[chestIdx][drawerIdx]

        CheckResult(newChests, (move == collisionDistance))
        chests = newChests
      # end of outmost for loop

    # exit()  # Used to try only one data point
    print "One data point done. Buckets on 2 levels:", nBucketsOnSplitLevel, \
      "Collision distance:", collisionDistance
  # end of while loop
# end of main()

def CheckResult(chests, expectCollision) :
  if debug: print "Allocation details. Expect collision:", expectCollision
  for chest in chests :
    if debug: print chest

  nBeansFromSameBucket = 0
  for chest in chests :
    c = {}  # To count number of beans from the same bucket
    for beanID in chest :
      if beanID % 2 == 1 : continue  # Don't count red beans
      bucketNum = BucketNum(beanID)
      c[bucketNum] = (c[bucketNum] + 1) if bucketNum in c else 1
    maxKey = max(c.iteritems(), key=operator.itemgetter(1))[0]
    nBeansFromSameBucket = max(nBeansFromSameBucket, c[maxKey])
    if debug: print c, c[maxKey]
  assert(expectCollision == (nBeansFromSameBucket >= 2))
# end of CheckResult()

global leading8, bucketPlex, beanPlex
leading8 = 8000000
bucketPlex = 10000
beanPlex = 10

def BeanID(bucketNum, beanNum, isRed) :
  return bucketNum * bucketPlex + beanNum * beanPlex + isRed + leading8

def BucketNum(beanID) :
  return beanID % leading8 / bucketPlex

def BeanNum(beanID) :
  return beanID % bucketPlex / beanPlex

def MakeData() :
  while True:
    redBeans = []  # 20 red beans
    buckets = [None] * 30  # 30 buckets of beans
    beanCount = 0

    # Bean ID: total 7 digits, a leading "8" for equal length beanID,
    # followed by bucket number (2 digits), bean mumber (3 digits) and
    # color (1 for red). Bucket and bean numbers start from 1 for easy reading
    def MakeBean(bucketNum, beanNum) :
      redBean = random.randint(0, 1) if len(redBeans) < 20 else 0  # Max 20 red
      beanID = BeanID(bucketNum, beanNum, redBean)
      redBeans.append(beanID) if redBean == 1 else None
      return beanID

    for i in range(0, 30) :  # Put one bean in each bucket at first
      beanCount += 1
      buckets[i] = [MakeBean(i + 1, beanCount)]

    while (beanCount < 100) :
      bucketIdx = random.randint(0, 29)  # The rest 70 beans in random buckets
      if len(buckets[bucketIdx]) < maxPerBucket :  # Still some room in bucket
        beanCount += 1
        buckets[bucketIdx].append(MakeBean(bucketIdx + 1, beanCount))

    if len(redBeans) < 20 :  # Not enough red beans (rare case), simply re-try
      if debug: print "# of red bean < 20. Will re-try", len(redBeans) 
    else :
      break
  # end of while loop

  CheckData(buckets, redBeans)
  return {"buckets": buckets,
          "redBeans": redBeans}
# end of MakeData()

def CheckData(buckets, redBeans) :
  redBeanCount = 0
  beans = []

  if debug: print "Buckets:"
  for bucket in buckets :
    if debug: print (buckets.index(bucket) + 1), bucket
    assert(len(bucket) <= maxPerBucket)  # Bucket size limit
    for beanID in bucket :
      redBeanCount += beanID % 2
      bisect.insort(beans, BeanNum(beanID))
      # All beans in a bucket have the same bucket number
      assert(buckets.index(bucket) + 1 == BucketNum(beanID))

  assert(redBeanCount == 20 and len(redBeans) == 20)
  assert(len(buckets) == 30 and len(beans) == 100)
  for beanNum in range(1, 101) :  # Beans have numbers from 1 to 100
    assert(beans[beanNum - 1] == beanNum)
# end of CheckData()

random.seed(datetime.now())
if __name__ == '__main__':
  main()
