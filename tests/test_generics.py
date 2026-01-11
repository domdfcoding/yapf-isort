# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from formate.reformat_generics import reformat_generics

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

example_3 = """
dtype = Literal["sphinx_rtd_theme", "sphinx-rtd-theme", "alabaster", "repo_helper_sphinx_theme",
				"repo-helper-sphinx-theme", "domdf_sphinx_theme", "domdf-sphinx-theme", "furo"]
"""

example_4 = """
class Foo:
	dtype = Literal["sphinx_rtd_theme", "sphinx-rtd-theme", "alabaster", "repo_helper_sphinx_theme",
					"repo-helper-sphinx-theme", "domdf_sphinx_theme", "domdf-sphinx-theme", "furo"]
"""


@pytest.mark.parametrize(
		"input",
		[
				pytest.param("Union[str, int, float]", id="Simple Union"),
				pytest.param("Mapping[str, int]", id="Simple Mapping"),
				pytest.param("List[str]", id="Simple List"),
				pytest.param("Tuple[int, int, str, float, str, int, bytes]", id="Simple Tuple"),
				pytest.param(
						"Tuple[int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes, int, int, str, float, str, int, bytes]",
						id="Long Tuple",
						),
				pytest.param("Optional[Callable[[Optional[str]], Any]]", id="Complex Optional"),
				pytest.param(
						"_ParamsMappingValueType = Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]]",
						id="Complex Alias 1",
						),
				pytest.param(
						"_Data = Union[None, str, bytes, MutableMapping[str, Any], Iterable[Tuple[str, Optional[str]]], IO]",
						id="Complex Alias 2",
						),
				pytest.param(example_1, id="Multiline 1"),
				pytest.param(example_1a, id="Multiline 1a"),
				pytest.param(example_2, id="Multiline 2"),
				pytest.param(example_3, id="Literal"),
				pytest.param(example_4, id="Literal in class"),
				],
		)
def test_generics(input: str, advanced_file_regression: AdvancedFileRegressionFixture):  # noqa: A002  # pylint: disable=redefined-builtin
	advanced_file_regression.check(reformat_generics(input), extension="._py")
