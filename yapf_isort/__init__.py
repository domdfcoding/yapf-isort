#!/usr/bin/env python3
#
#  __init__.py
"""
yapf 💌 isort
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  License: Apache Software License 2.0
#  See the LICENSE file for details.
#

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "Apache Software License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

# stdlib
import difflib
from typing import Optional, Sequence

# 3rd party
import isort  # type: ignore
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.terminal_colours import Colour, Fore
from domdf_python_tools.typing import PathLike
from isort import Config
from yapf.yapflib.yapf_api import FormatCode  # type: ignore

__all__ = ["coloured_diff", "Reformatter", "reformat_file"]


def coloured_diff(
		a: Sequence[str],
		b: Sequence[str],
		fromfile: str = '',
		tofile: str = '',
		fromfiledate: str = '',
		tofiledate: str = '',
		n: int = 3,
		lineterm: str = '\n',
		removed_colour: Colour = Fore.RED,
		added_colour: Colour = Fore.GREEN,
		changed_colour: Colour = Fore.BLUE,
		) -> str:
	r"""
	Compare two sequences of lines; generate the delta as a unified diff.

	Unified diffs are a compact way of showing line changes and a few
	lines of context.  The number of context lines is set by 'n' which
	defaults to three.

	By default, the diff control lines (those with ---, +++, or @@) are
	created with a trailing newline.  This is helpful so that inputs
	created from file.readlines() result in diffs that are suitable for
	file.writelines() since both the inputs and outputs have trailing
	newlines.

	For inputs that do not have trailing newlines, set the lineterm
	argument to "" so that the output will be uniformly newline free.

	The unidiff format normally has a header for filenames and modification
	times.  Any or all of these may be specified using strings for
	'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
	The modification times are normally expressed in the ISO 8601 format.

	Example:

	>>> for line in coloured_diff('one two three four'.split(),
	...             'zero one tree four'.split(), 'Original', 'Current',
	...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
	...             lineterm=''):
	...     print(line)                 # doctest: +NORMALIZE_WHITESPACE
	--- Original        2005-01-26 23:30:50
	+++ Current         2010-04-02 10:20:52
	@@ -1,4 +1,4 @@
	+zero
	one
	-two
	-three
	+tree
	four

	:param a:
	:param b:
	:param fromfile:
	:param tofile:
	:param fromfiledate:
	:param tofiledate:
	:param n:
	:param lineterm:
	:param removed_colour:
	:param added_colour:

	:return:
	"""

	buf = StringList()
	diff = difflib.unified_diff(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm)

	for line in diff:
		if line.startswith('+'):
			buf.append(added_colour(line))
		elif line.startswith('-'):
			buf.append(removed_colour(line))
		elif line.startswith('^'):
			buf.append(changed_colour(line))
		else:
			buf.append(line)

	buf.blankline(ensure_single=True)

	return str(buf)


class Reformatter:
	"""
	Reformat a Python source file.

	:param filename:
	:param yapf_style:
	:param isort_config:
	"""

	def __init__(self, filename: PathLike, yapf_style: str, isort_config: Config):
		self.filename = str(filename)
		self.file_to_format = PathPlus(filename)
		self.yapf_style = yapf_style
		self.isort_config = isort_config
		self._unformatted_source = self.file_to_format.read_text()
		self._reformatted_source: Optional[str] = None

	def run(self) -> bool:
		"""
		Run the reformatter.

		:return: Whether the file was changed.
		"""

		yapfed_code = FormatCode(self._unformatted_source, style_config=self.yapf_style)[0]
		self._reformatted_source = isort.code(yapfed_code, config=self.isort_config)
		return self._reformatted_source != self._unformatted_source

	def get_diff(self) -> str:
		"""

		:return:
		"""

		# Based on yapf
		# Apache 2.0 License

		if self._reformatted_source is None:
			raise ValueError("'Reformatter.run()' must be called first!")

		before = self._unformatted_source.splitlines()
		after = self._reformatted_source.splitlines()
		return coloured_diff(
				before,
				after,
				self.filename,
				self.filename,
				'(original)',
				'(reformatted)',
				lineterm='',
				)

	def to_string(self) -> str:
		"""
		Return the reformatted file as a string.
		"""

		if self._reformatted_source is None:
			raise ValueError("'Reformatter.run()' must be called first!")

		return self._reformatted_source

	def to_file(self) -> None:
		"""
		Write the reformatted source to the original file.
		"""

		if self._reformatted_source is None:
			raise ValueError("'Reformatter.run()' must be called first!")

		self.file_to_format.write_clean(self._reformatted_source)


def reformat_file(filename: PathLike, yapf_style: str, isort_config_file: str) -> int:
	"""
	Reformat the given file.

	:param filename:
	:param yapf_style:
	:param isort_config_file:

	:return:
	"""

	isort_config = Config(settings_file=str(isort_config_file))

	r = Reformatter(filename, yapf_style, isort_config)

	if r.run():
		print(r.get_diff())
		ret = 1
	else:
		ret = 0

	r.to_file()

	return ret
