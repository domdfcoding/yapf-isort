#!/usr/bin/env python3
#
#  __main__.py
"""
yapf 💌 isort
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  License: Apache Software License 2.0
#  See the LICENSE file for details.
#

# stdlib
import argparse
import fnmatch
import re
import sys
from typing import List, Optional

# 3rd party
from domdf_python_tools.paths import PathPlus

# this package
from yapf_isort import reformat_file

__all__ = ["main"]


def main(argv: Optional[List[str]] = None) -> int:
	"""

	:param argv:

	:return:
	"""

	parser = argparse.ArgumentParser(description="yapf 💌 isort")
	parser.add_argument("filename", type=str, nargs="+", metavar="FILENAME")
	parser.add_argument(
			"--yapf-style",
			type=str,
			help="The name of the yapf style to use, or the path to a style file. (default: %(default)s)",
			default=".style.yapf"
			)
	parser.add_argument(
			"--isort-config",
			type=PathPlus,
			help="The path to the isort configuration file. (default: %(default)s)",
			default=".isort.cfg"
			)
	parser.add_argument(
			'-e',
			'--exclude',
			metavar='PATTERN',
			action='append',
			default=None,
			help='patterns for files to exclude from formatting'
			)

	args = parser.parse_args(argv)

	retv = 0

	for filename in args.filename:
		for pattern in args.exclude or []:
			if re.match(fnmatch.translate(pattern), str(filename)):
				continue

		retv |= reformat_file(filename, yapf_style=args.yapf_style, isort_config_file=args.isort_config)

	return retv


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
