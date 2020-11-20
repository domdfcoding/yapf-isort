#!/usr/bin/env python

# stdlib
import pathlib
import sqlite3

# 3rd party
from domdf_python_tools.typing import PathLike


def fixup_coverage(
		old_base: PathLike,
		new_base: PathLike,
		coverage_filename: PathLike = ".coverage",
		):
	"""
	Replaces the start of filenames in .coverage files.

	:param old_base:
	:param new_base:
	:param coverage_filename:
	"""

	conn = sqlite3.connect(str(coverage_filename))
	c = conn.cursor()

	old_base = pathlib.Path(old_base)
	new_base = pathlib.Path(new_base)

	for (idx, filename) in c.execute("SELECT * FROM file").fetchall():

		if not filename.startswith(str(old_base)):
			continue

		new_filename = str(new_base / pathlib.Path(filename).relative_to(old_base))
		c.execute("UPDATE file SET path=? WHERE id=?", (new_filename, idx))

	conn.commit()
	conn.close()


if __name__ == "__main__":
	repo_name = import_name = "yapf-isort"
	fixup_coverage(f"/home/runner/work/{repo_name}/{import_name}", '')
