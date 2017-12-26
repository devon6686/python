#!/usr/bin/env python3
"""
使用bisect模块，插入一个数字到一个排序的序列中的位置；
"""
import bisect
import sys


HAYSTACK = [1, 2, 4, 5, 8, 11, 13, 14, 17, 19, 22, 25, 28, 31, 33, 38, 40]
NEEDLES = [0, 2, 4, 6, 10, 12, 14, 19, 23, 25, 29, 33, 36, 39, 41]

ROW_FMT = '{0:2d} @ {1:2d}    {2}{0:<2d}'


def demo(bisect_fn):
	for needle in reversed(NEEDLES):
		position = bisect_fn(HAYSTACK, needle)
		offset = position*'  |'
		print(ROW_FMT.format(needle, position, offset))


if __name__ == '__main__':
	if sys.argv[-1] == 'left':
		bisect_fn = bisect.bisect_left
	else:
		bisect_fn = bisect.bisect

	print("DEMO:", bisect_fn.__name__)
	print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
	demo(bisect_fn)