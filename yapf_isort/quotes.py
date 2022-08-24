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

# 3rd party
from domdf_python_tools.utils import double_repr_string
from formate.dynamic_quotes import QuoteRewriter, dynamic_quotes

__all__ = ["Visitor", "double_repr", "reformat_quotes"]

Visitor = QuoteRewriter
double_repr = double_repr_string
reformat_quotes = dynamic_quotes
