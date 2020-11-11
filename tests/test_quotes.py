# 3rd party
import pytest

# this package
from yapf_isort.quotes import reformat_quotes

value_1 = """\
status_codes: Dict[str, str] = {
		"add": "A",
		"delete": "D",
		"modify": "M",
		}
"""

expected_1 = """\
status_codes: Dict[str, str] = {
		"add": 'A',
		"delete": 'D',
		"modify": 'M',
		}
"""


@pytest.mark.parametrize(
		"value, expects",
		[
				("'hello world'", '"hello world"'),
				("''", "''"),
				('""', "''"),
				("'a'", "'a'"),
				('"a"', "'a'"),
				("'Z'", "'Z'"),
				('"Z"', "'Z'"),
				("'5'", "'5'"),
				('"5"', "'5'"),
				("'\u2603'", "'\u2603'"),
				("'user'", '"user"'),
				('"☃"', "'\u2603'"),
				('print(123)\n"☃"', "print(123)\n'☃'"),
				('"☃"\nprint(123)', "'☃'\nprint(123)"),
				("'hello\\nworld'", "'hello\\nworld'"),
				('"hello\\nworld"', '"hello\\nworld"'),
				('"\\""', "'\"'"),
				('"quote \\""', "'quote \"'"),
				("'\\''", "\"'\""),
				("'quote \\''", "\"quote '\""),
				(value_1, expected_1),
				]
		)
def test_quotes(value, expects):
	assert reformat_quotes(value) == expects
