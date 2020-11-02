#!/usr/bin/env python3
#
#  generics.py
"""
Reformatter for generics.

E.g.:

.. code-block:: python

	Union[List[str], List[float], Dict[str, float], None]
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  License: Apache Software License 2.0
#  See the LICENSE file for details.
#

# stdlib
import ast
import typing
from collections.abc import Collection
from io import StringIO
from textwrap import indent
from typing import Any, Sequence, Union

# 3rd party
import asttokens  # type: ignore
from domdf_python_tools.stringlist import DelimitedList

__all__ = ["Generic", "List", "Visitor", "UnionVisitor", "reformat_generics"]

collection_types = {"Union", "List", "Tuple", "Set", "Dict", "Callable", "Optional"}

subclasses = [Collection]
while subclasses:
	subclass = subclasses.pop(0)
	if subclass.__module__ == "collections.abc":
		collection_types.add(subclass.__name__)
		subclasses.extend(subclass.__subclasses__())


class Generic:

	def __init__(self, name: str, elements: Sequence[Union[str, "Generic"]]):
		self.name = str(name)
		self.elements = DelimitedList(elements)  # type: ignore

	def __repr__(self) -> str:
		return f"{self.name}[{self.elements:, }]"

	def format(self, line_offset: int = 0) -> str:
		if line_offset + len(repr(self)) > 110:
			# Line too long as is
			elements = DelimitedList()
			for element in self.elements:
				if isinstance(element, Generic):
					elements.append(indent(element.format(line_offset + 4), "\t"))
				else:
					elements.append(indent(str(element), "\t"))
			return f"{self.name}[\n{elements:,\n}\n	]"
		else:
			return repr(self)


class List:

	def __init__(self, elements: Sequence[Union[str, Generic]]):
		self.elements = DelimitedList(elements)  # type: ignore

	def __repr__(self) -> str:
		return f"[{self.elements:, }]"


class Visitor(ast.NodeVisitor):

	def __init__(self):
		self.unions: typing.List[typing.Tuple[ast.Subscript, Generic]] = []

	def visit_Subscript(self, node: ast.Subscript) -> Any:
		if isinstance(node.value, ast.Name) and node.value.id in collection_types:
			union = Generic(node.value.id, UnionVisitor().visit(node.slice.value))  # type: ignore
			self.unions.append((node, union))
		else:
			self.generic_visit(node)

	def visit(self, node: ast.AST) -> typing.List[typing.Tuple[ast.Subscript, Generic]]:
		super().visit(node)
		return self.unions

	def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
		return None

	def visit_ClassDef(self, node: ast.ClassDef) -> Any:
		return None

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
		return None


class UnionVisitor(ast.NodeVisitor):

	def __init__(self):
		super().__init__()
		self.structure = []

	def generic_visit(self, node: ast.AST) -> Any:
		super().generic_visit(node)

	def visit_Name(self, node: ast.Name) -> Any:
		self.structure.append(f"{node.id}")

	def visit_Attribute(self, node: ast.Attribute) -> Any:
		parts = DelimitedList()
		value: Union[ast.Name, ast.expr] = node.value

		while True:
			if isinstance(value, ast.Name):
				parts.append(value.id)
				break
			elif isinstance(value, ast.Attribute):
				value = value.attr  # type: ignore
			else:
				raise NotImplementedError

		self.structure.append(f"{parts:.}.{node.attr}")

	def visit_Subscript(self, node: ast.Subscript) -> Any:
		union = Generic(
				node.value.id,  # type: ignore
				UnionVisitor().visit(node.slice.value),  # type: ignore
				)
		self.structure.append(union)

	def visit_List(self, node: ast.List) -> Any:
		elements = []
		for child in node.elts:
			elements.extend(UnionVisitor().visit(child))
		self.structure.append(List(elements))

	def visit_Load(self, node: ast.Load) -> None:
		return None

	def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
		return None

	def visit_ClassDef(self, node: ast.ClassDef) -> Any:
		return None

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
		return None

	def visit_Ellipsis(self, node: ast.Ellipsis) -> Any:
		self.structure.append("...")

	def visit_NameConstant(self, node: ast.NameConstant) -> Any:
		self.structure.append(node.value)

	def visit_Str(self, node: ast.Str) -> Any:
		self.structure.append(f'"{node.s}"')

	def visit(self, node: ast.AST) -> Any:
		super().visit(node)
		return self.structure


def reformat_generics(source: str) -> str:
	"""
	Reformats generics in the given source, and returns the reformatted source.

	:param source:
	"""

	offset = 0
	buf = StringIO()
	visitor = Visitor()
	atok = asttokens.ASTTokens(source, parse=True)

	try:
		for union_node, union_obj in visitor.visit(atok.tree):
			text_range = atok.get_text_range(union_node)
			buf.write(source[offset:text_range[0]])

			reversed_line = source[offset:text_range[0]][::-1]

			if "\n" in reversed_line:
				line_offset = reversed_line.index("\n")
			else:
				line_offset = 0

			buf.write(union_obj.format(line_offset))
			offset = text_range[1]

		buf.write(source[offset:])

		return buf.getvalue()

	except NotImplementedError as e:
		print(f"An error occurred: {e}")
		return source
