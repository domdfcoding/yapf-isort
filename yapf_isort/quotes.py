#!/usr/bin/env python3
#
#  quotes.py
"""
Reformatter for quotes.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  License: Apache Software License 2.0
#  See the LICENSE file for details.
#

# stdlib
import ast
import json
import re
from io import StringIO
from typing import List

# 3rd party
import asttokens  # type: ignore

__all__ = ["Visitor", "double_repr", "reformat_quotes"]


class Visitor(ast.NodeVisitor):  # noqa: D101

	def __init__(self):
		super().__init__()
		self.string_nodes: List[ast.Str] = []

	def visit_Str(self, node: ast.Str) -> None:  # noqa: D102
		self.string_nodes.append(node)

	def visit(self, node: ast.AST) -> List[ast.Str]:  # noqa: D102
		super().visit(node)
		return self.string_nodes


def double_repr(string: str):
	"""
	Like :func:`repr`, but tries to use double quotes instead.
	"""

	# figure out which quote to use; double is preferred
	if '"' in string and "'" not in string:
		return repr(string)
	else:
		return json.dumps(string, ensure_ascii=False)


def reformat_quotes(source: str) -> str:
	"""
	Reformats quotes in the given source, and returns the reformatted source.

	:param source:
	"""

	offset = 0
	buf = StringIO()
	visitor = Visitor()
	atok = asttokens.ASTTokens(source, parse=True)

	def key_func(value):
		return atok.get_text_range(value)[0]

	try:
		for string_node in sorted(visitor.visit(atok.tree), key=key_func):
			text_range = atok.get_text_range(string_node)

			if text_range == (0, 0):
				continue

			buf.write(source[offset:text_range[0]])

			if source[text_range[0]:text_range[1]] in {'""', "''"}:
				buf.write("''")
			elif not re.match("^[\"']", source[text_range[0]:text_range[1]]):
				buf.write(source[text_range[0]:text_range[1]])
			elif len(string_node.s) == 1:
				buf.write(repr(string_node.s))
			elif '\n' in source[text_range[0]:text_range[1]]:
				buf.write(source[text_range[0]:text_range[1]])
			elif '\n' in string_node.s or "\\n" in string_node.s:
				buf.write(source[text_range[0]:text_range[1]])
			else:
				buf.write(double_repr(string_node.s))

			offset = text_range[1]

		buf.write(source[offset:])

		return buf.getvalue()

	except NotImplementedError as e:  # pragma: no cover
		print(f"An error occurred: {e}")
		return source
