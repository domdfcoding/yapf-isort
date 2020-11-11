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

# stdlib
from typing import Optional

# 3rd party
import click
import isort  # type: ignore
from consolekit.terminal_colours import resolve_color_default
from consolekit.utils import coloured_diff
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from isort import Config
from yapf.yapflib.yapf_api import FormatCode  # type: ignore

# this package
from yapf_isort.generics import reformat_generics
from yapf_isort.quotes import reformat_quotes

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "Apache Software License"
__version__: str = "0.5.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Reformatter", "reformat_file"]

# TODO: options for no colours in output and no diff when changes made.


class Reformatter:
	"""
	Reformat a Python source file.

	:param filename:
	:param yapf_style: The name of the yapf style, or the path to the yapf style file.
	:param isort_config: The filename of the isort configuration file.
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

		quote_formatted_code = reformat_quotes(self._unformatted_source)
		yapfed_code = FormatCode(quote_formatted_code, style_config=self.yapf_style)[0]
		generic_formatted_code = reformat_generics(yapfed_code)
		# TODO: support spaces
		isorted_code = StringList(isort.code(generic_formatted_code, config=self.isort_config))
		isorted_code.blankline(ensure_single=True)
		self._reformatted_source = str(isorted_code)
		# self._reformatted_source = quote_formatted_code

		return self._reformatted_source != self._unformatted_source

	def get_diff(self) -> str:
		"""
		Returns the diff between the original and reformatted file content.
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
				"(original)",
				"(reformatted)",
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

		self.file_to_format.write_text(self._reformatted_source)


def reformat_file(filename: PathLike, yapf_style: str, isort_config_file: PathLike) -> int:
	"""
	Reformat the given file.

	:param filename:
	:param yapf_style:
	:param isort_config_file:
	"""

	isort_config = Config(settings_file=str(isort_config_file))

	r = Reformatter(filename, yapf_style, isort_config)

	if r.run():
		click.echo(r.get_diff(), color=resolve_color_default())
		ret = 1
	else:
		ret = 0

	r.to_file()

	return ret
