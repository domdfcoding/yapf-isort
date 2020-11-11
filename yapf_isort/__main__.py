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
import fnmatch
import re
import sys
from typing import List, Optional

# 3rd party
import click
from consolekit import click_command
from domdf_python_tools.paths import PathPlus

# this package
from yapf_isort import reformat_file

__all__ = ["main"]


@click.argument("filename", type=click.STRING, nargs=-1)
@click.option(
		"--yapf-style",
		type=click.STRING,
		help="The name of the yapf style to use, or the path to a style file.",
		default=".style.yapf",
		show_default=True,
		)
@click.option(
		"--isort-config",
		type=PathPlus,
		help="The path to the isort configuration file.",
		default=".isort.cfg",
		show_default=True,
		)
@click.option(
		"-e",
		"--exclude",
		metavar="PATTERN",
		type=list,
		default=None,
		help="patterns for files to exclude from formatting",
		)
@click_command()
def main(
		filename: str,
		yapf_style: str,
		isort_config: PathPlus,
		exclude: Optional[List[str]],
		):
	"""
	yapf 💌 isort
	"""

	retv = 0

	for path in filename:
		for pattern in exclude or []:
			if re.match(fnmatch.translate(pattern), str(path)):
				continue

		retv |= reformat_file(path, yapf_style=yapf_style, isort_config_file=isort_config)

	sys.exit(retv)


if __name__ == "__main__":
	sys.exit(main())
