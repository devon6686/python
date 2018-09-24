#!/usr/bin/env python3
"""
replace settings file path of product package(war, jar) and re-archive packages for dmz-cloud environment
war: 'WEB-INF/classes/spring-config.xml'
jar: 'spring-config.xml'
pattern: 'nfs/wanjia/settings' -> 'nfs/wanjia/cloud-settings'
"""

import argparse
import configparser
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


def make_package(pkg, configfile, workdir, keyword='nfs/wanjia/settings', srcdir='/data', dstdir='/project/cloud/data'):
	def unarchive_pkg(srcpkg, workdir):
		flag = True
		if Path(srcpkg).exists():
			shutil.rmtree(workdir) if Path(workdir).exists() else print('Dir: {} will be delete'.format(workdir))
			Path(workdir).mkdir(parents=True)
			shutil.copy2(srcpkg, workdir)
			if Path(workdir).exists():
				with ZipFile(srcpkg) as zf:
					zf.extractall(workdir)
				print('succeed unarchive package: {}'.format(srcpkg))
		else:
			flag = False
			print('Error! src pkg: {} not found'.format(srcpkg))
		return flag

	def rep_conf_file(conf_file, keyword: str, oldstr='settings', newstr='cloud-settings'):
		flag = True
		pattern = re.compile(keyword)
		dst_file = str(Path(workdir) / Path(conf_file))
		if Path(dst_file).exists():
			new_conf_file = dst_file + '.new'
			with open(new_conf_file, mode='a+') as nf:
				with open(dst_file) as of:
					for line in of:
						if pattern.findall(line):
							line = line.replace(oldstr, newstr)
						nf.write(line)
			Path(new_conf_file).rename(dst_file)
		else:
			flag = False
			print('Error! config file: {} not found'.format(str(conf_file)))
		return flag

	def archive_pkg(pkg, workdir, config_file):
		os.chdir(workdir)
		zf = ZipFile(pkg, 'a')
		zf.write(config_file)
		zf.close()
		shutil.copy(pkg, dst_dir)
		print('New Package: {}'.format(pkg))
		print('>>' * 20)

	src_pkg = str(Path(srcdir) / Path(pkg))

	if unarchive_pkg(src_pkg, workdir):
		if len(configfile) == 1:
			archive_pkg(pkg, workdir, configfile) if rep_conf_file(configfile, keyword) else print('Error')
		else:
			for conf_file in configfile:
				archive_pkg(pkg, workdir, conf_file) if rep_conf_file(conf_file, keyword) else print('Error')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='replcae spring-config.xml')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-p', metavar='project_name', dest='project', help='project name')
	group.add_argument('-a', action='store_true', dest='all', help='all projects')
	args = parser.parse_args()

	cfg = configparser.ConfigParser()
	project_file = "projects.ini"
	cfg.read(project_file)

	dst_dir = '/project/cloud/data'
	print(args)
	if args.all:
		print('Replace All projects')
		print('--' * 20)
		fail_pkg = []
		success_pkg = []
		for project in cfg.sections():
			pkg_name = cfg.get(project, 'package')
			config = cfg.get(project, 'configFile').split(',')
			flag = datetime.now().strftime('%Y%m%d/%H%M%S')
			ts = datetime.now().strftime('%Y%m%d/%H%M%S')
			workdir = str(Path(dst_dir) / Path(ts))
			try:
				make_package(pkg_name, config, workdir)
			except:
				fail_pkg.append(pkg_name)
			else:
				success_pkg.append(pkg_name)
		print('Success Projects: ', success_pkg)
		print('Failed Projects: ', fail_pkg)
	else:
		pkg_name = cfg.get(args.project, 'package')
		config = cfg.get(args.project, 'configFile').split(',')
		ts = datetime.now().strftime('%Y%m%d/%H%M%S')
		workdir = str(Path(dst_dir) / Path(ts))
		print('pkg: {} config_file: {} workdir:{}'.format(pkg_name, config, workdir))
		make_package(pkg_name, config, workdir)
