#!/usr/bin/env python3
#
#  __main__.py
"""
yapf 💌 isort.
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
from typing import Iterable, List, Optional

# 3rd party
import click
from consolekit import click_command
from consolekit.options import auto_default_option

# this package
from yapf_isort import reformat_file

__all__ = ["main"]


@auto_default_option(
		"-e",
		"--exclude",
		metavar="PATTERN",
		type=list,
		help="patterns for files to exclude from formatting",
		)
@auto_default_option(
		"--isort-config",
		type=click.STRING,
		help="The path to the isort configuration file.",
		show_default=True,
		)
@auto_default_option(
		"--yapf-style",
		type=click.STRING,
		help="The name of the yapf style to use, or the path to a style file.",
		show_default=True,
		)
@click.argument("filename", type=click.STRING, nargs=-1)
@click_command()
def main(
		filename: Iterable[str],
		yapf_style: str = ".style.yapf",
		isort_config: str = ".isort.cfg",
		exclude: Optional[List[str]] = None,
		):
	"""
	yapf 💌 isort.
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
