#!/usr/bin/env python
# -*- coding: utf-8 -*-

# items.py should be in the same folder
from items import item_color

# helper function for distinct check
def are_exclusive(keys, items):
        sets = [ items[k] for k in keys ]
        return not bool(set.intersection(*sets))

# helper function for union
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

# first problem
# @param dict items
# @return list
def max_cover_inclusive(items):
        solns = {}
        for key in items:
                i = items.copy()
                (covered, keys) = (i[key], [key])
                while True:
                        key = get_max_uncover_inclusive_item(covered, i)
                        if not key:
                                t = len(covered)
                                if t in solns and len(solns[t]) < len(keys): break
                                solns[t] = keys
                                break
                        covered = covered.union(i.pop(key))
                        keys.append(key)
        return solns[max(solns)]

# second problem
# @param dict items
# @return list
def max_cover_exclusive(items):
        solns = {}
        for key in items:
                i = items.copy()
                (covered, keys) = (i[key], [key])
                while True:
                        key = get_max_uncover_exclusive_item(covered, i)
                        if not key:
                                t = len(covered)
                                if t in solns and len(solns[t]) < len(keys): break
                                solns[t] = keys
                                break
                        covered = covered.union(i.pop(key))
                        keys.append(key)
        return solns[max(solns)]

# third problem
# @param int k
# @param dict items
# @return list
def max_cover_k(k, items):
        solns = {}
        for key in items:
                i = items.copy()
                (covered, keys) = (i[key], [key])
                while len(keys) < k:
                        key = get_max_uncover_exclusive_item(covered, i)
                        if not key:
                                t = len(covered)
                                if t in solns and len(solns[t]) < len(keys): break
                                solns[t] = keys
                                break
                        covered = covered.union(i.pop(key))
                        keys.append(key)
                        t = len(covered)
                        if t in solns and len(solns[t]) < len(keys): pass
                        solns[len(covered)] = keys
        return solns[max(solns)]

# -*- case tests -*-

# first case test
def test_max_cover_inclusive(items):
        print "Current testcase: {}".format(test_max_cover_inclusive.__name__)
        result = max_cover_inclusive(items)
        ex = "True" if are_exclusive(result, items) else "False"
        u = len(result)
        l = len(union(result, items))
        print "Exclusive: {} | Keys: {} | Covered: {}".format(ex, u, l)
        print result

# second case test
def test_max_cover_exclusive(items):
        print "Current testcase: {}".format(test_max_cover_exclusive.__name__)
        result = max_cover_exclusive(items)
        ex = "True" if are_exclusive(result, items) else "False"
        u = len(result)
        l = len(union(result, items))
        print "Exclusive: {} | Keys: {} | Covered: {}".format(ex, u, l)
        print result

# third case test
def test_max_cover_k(k, items):
        print "Current testcase: {}".format(test_max_cover_k.__name__)
        result = max_cover_k(k, items)
        ex = "True" if are_exclusive(result, items) else "False"
        u = len(result)
        l = len(union(result, items))
        print "Exclusive: {} | Keys: {} | Covered: {}".format(ex, u, l)
        print result

# main entry
if __name__ == '__main__':
        # test cases
        test_max_cover_inclusive(item_color)
        test_max_cover_exclusive(item_color)
        test_max_cover_k(5, item_color)

        #https://github.com/songmw90/SKKU/blob/master/ECE5924/colors.py