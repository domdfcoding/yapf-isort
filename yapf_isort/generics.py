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

# 3rd party
from formate.reformat_generics import Generic, List, UnionVisitor, Visitor, reformat_generics

__all__ = ["Generic", "List", "Visitor", "UnionVisitor", "reformat_generics"]
