#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# items.py should be in the same folder
from items import item_color
from collections import OrderedDict
 
def are_exclusive(keys, items):
        sets = [ items[k] for k in keys ]
        return not bool(set.intersection(*sets))
 
def union(keys, items):
        sets = [ items[k] for k in keys ]
        return set.union(*sets)
 
# helper function: greedy inclusive maximum uncovered values
# @param set current
# @param dict items
# @return string
def get_max_uncover_inclusive_item(current, items):
        (max_diff, key) = (0, '')
        for k in items:
                diff = len(items[k].difference(current))
                if max_diff < diff:
                        max_diff = diff
                        key = k
        return key
 
# helper function: greedy exclusive maximum uncovered values
# @param set current
# @param dict items
# @return string
def get_max_uncover_exclusive_item(current, items):
        (max_diff, key) = (0, '')
        for k in items:
                if items[k].isdisjoint(current):
                        diff = len(items[k].difference(current))
                        if max_diff < diff:
                                max_diff = diff
                                key = k
        return key
 
# first function
# @param dict items
# @return list
def max_cover_inclusive(items):
        items = items.copy()
        (covered, keys) = (set(), list())
        while True:
                key = get_max_uncover_inclusive_item(covered, items)
                if not key: return keys
                covered = covered.union(items.pop(key))
                keys.append(key)
 
# second function
# @param dict items
# @return list
def max_cover_exclusive(items):
        solns = {}
        # greedy algorithm start from each value
        for k in items:
                i = items.copy()
                # initial row
                (covered, keys) = (items[k], [k])
                while True:
                        key = get_max_uncover_exclusive_item(covered, i)
                        if not key:
                                solns[len(covered)] = keys
                                break
                        covered = covered.union(i.pop(key))
                        keys.append(key)
        return solns[max(solns, key=int)]
 
# third function
# @param int k
# @param dict items
# @return list
def max_cover_k(k, items):
        items = items.copy()
        (covered, keys) = (set(), list())
        while len(keys) < k:
                key = get_max_uncover_inclusive_item(covered, items)
                covered = covered.union(items.pop(key))
                keys.append(key)
        return keys
 
# main entry
if __name__ == '__main__':

        # test cases
        cases = OrderedDict()
        cases['max_cover_inclusive'] = [item_color]
        cases['max_cover_exclusive'] = [item_color]
        cases['max_cover_k'] = [5, item_color]
 
        # test each case
        for case in cases:
                #print 'Current testcase: {}'.format(case) #if using Python 2.7 higher
                params = cases[case]
                fn = locals()[case]
                result = fn(*params)

        result1 = max_cover_inclusive(item_color)
        result2 = max_cover_exclusive(item_color)
        result3 = max_cover_k(30, item_color)
        all_values1 = union(result1, item_color);

        print(str(len(result1)) + "-" + str(len(all_values1)))
        print(result1)
        
        all_values2 = union(result2, item_color);
        print(str(len(result2)) + "-" + str(len(all_values2)))
        print(result2)
        
        all_values3 = union(result3, item_color);
        print(str(len(result3)) + "-" +  str(len(all_values3)))
        print(result3)

        #https://github.com/songmw90/SKKU/blob/master/ECE5924/colors.py