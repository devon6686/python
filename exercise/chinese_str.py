#!/usr/bin/env python3
from pathlib import Path
import re


def check_chinese(file: str, regex):
	try:
		with open(file, "r", encoding='utf-8') as f:
			for line in f:
				num = 0
				rt = regex.findall(line)
				if rt:
					num += len(rt)
					print("\tchinese:", end=" ")
					print(rt)
					# for content in rt:
					# 	print("\t{}".format(content))
				if num > 1:
					print("\nRESULT:\n\tFile: {}\tLineNumber:{}\n".format(file, num))
	except UnicodeDecodeError as e:
		print("File: {} could not be decoding with 'utf-8'".format(file))


def check_file(file_path: Path, regex1, regex2):
	if file_path.is_dir():
		for file in file_path.iterdir():
			if file.is_file():
				if not regex1.match(str(file)):
					check_chinese(str(file), regex2)
			elif file.is_dir():
				check_file(file, regex1, regex2)
	elif file_path.is_file():
		if not regex1.match(str(file_path)):
			check_chinese(file_path, regex2)


f1 = "/Users/devon/Desktop/project/"
pattern1 = '.*(\/\.|\.pyc).*'
regex1 = re.compile(pattern1)

pattern2 = '[\u4e00-\u9fa5]+'  # 中文字符
regex2 = re.compile(pattern2)

check_file(Path(f1), regex1, regex2)