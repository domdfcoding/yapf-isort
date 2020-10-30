import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from yapf_isort.generics import reformat_generics


example_1 = """
_ConvertibleType = Union[
		type,
		ParamType,
		Tuple[Union[type, ParamType], ...],
		Callable[[str], Any],
		Callable[[Optional[str]], Any],
		]
"""

example_1a = """
_ConvertibleType = Union[type, ParamType, Tuple[Union[type, ParamType], ...], Callable[[str], Any], Callable[[Optional[str]], Any]]
"""

example_2 = """
_ParamsType = Optional[Union[Mapping[Union[str, bytes, int, float], "_ParamsMappingValueType"],
								Union[str, bytes],
								Tuple[Union[str, bytes, int, float], "_ParamsMappingValueType"], ]]
"""


@pytest.mark.parametrize("input", [
		"Union[str, int, float]",
		"Mapping[str, int]",
		"List[str]",
		"Tuple[int, int, str, float, str, int, bytes]",
		"Optional[Callable[[Optional[str]], Any]]",
		"_ParamsMappingValueType = Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]]",
		"_Data = Union[None, str, bytes, MutableMapping[str, Any], Iterable[Tuple[str, Optional[str]]], IO]",
		"Tuple[int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes]",
		example_1,
		example_1a,
		example_2,
		])
def test_generics(input, file_regression: FileRegressionFixture):
	file_regression.check(reformat_generics(input), encoding="UTF-8", extension="._py")
