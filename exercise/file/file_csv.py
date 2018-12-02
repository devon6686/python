#!/usr/bin/env python3

from pathlib import Path
import csv

file = '/tmp/test.csv'
p = Path(file)


with open(str(p)) as f:
	reader = csv.reader(f)
	print(next(reader))
	print(next(reader))

row = ['1', 'jim', '22', 'China']
rows = [
	('2', 'tom', '18', 'Japan'),
	('3', 'lisa', '20', 'Africa')
]

with open(str(p), mode='a+') as f:
	write = csv.writer(f)
	write.writerow(row)
	write.writerows(rows)