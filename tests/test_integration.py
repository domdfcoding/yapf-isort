# stdlib
import re
from typing import Iterator, Union, no_type_check

# 3rd party
import isort
import pytest
from _pytest.capture import CaptureResult
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from consolekit.terminal_colours import strip_ansi
from consolekit.testing import CliRunner, Result
from domdf_python_tools.paths import PathPlus, in_directory
from isort import Config

# this package
from yapf_isort import Reformatter, reformat_file
from yapf_isort.__main__ import main

path_sub = re.compile(rf" .*/pytest-of-.*/pytest-\d+")


@no_type_check
def check_out(
		result: Union[Result, CaptureResult[str]],
		advanced_data_regression: AdvancedDataRegressionFixture,
		) -> None:

	if hasattr(result, "stdout"):
		stdout = result.stdout
	else:
		stdout = result.out

	if hasattr(result, "stderr"):
		stderr = result.stderr
	else:
		stderr = result.err

	data_dict = {
			"out": strip_ansi(path_sub.sub(" ...", stdout)).split('\n'),
			"err": strip_ansi(path_sub.sub(" ...", stderr)).split('\n'),
			}

	advanced_data_regression.check(data_dict)


@pytest.fixture()
def demo_environment(tmp_pathplus: PathPlus) -> Iterator[None]:

	code = [
			"class F:",
			"\tfrom collections import (",
			"Iterable,",
			"\tCounter,",
			"\t\t)",
			'',
			"\tdef foo(self):",
			"\t\tpass",
			'',
			"print('hello world')",
			]

	(tmp_pathplus / "code.py").write_lines(code, trailing_whitespace=True)

	old_isort_settings = isort.settings.CONFIG_SECTIONS.copy()

	try:
		isort.settings.CONFIG_SECTIONS["isort.cfg"] = ("settings", "isort")
		yield

	finally:
		isort.settings.CONFIG_SECTIONS = old_isort_settings


@pytest.fixture()
def isort_config_file() -> str:
	return str(PathPlus(__file__).parent / "isort.cfg")


@pytest.fixture()
def yapf_style() -> str:
	return str(PathPlus(__file__).parent / "style.yapf")


@pytest.mark.usefixtures("demo_environment")
def test_integration(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		capsys,
		advanced_data_regression: AdvancedDataRegressionFixture,
		isort_config_file: str,
		yapf_style: str,
		):

	assert reformat_file(tmp_pathplus / "code.py", yapf_style=yapf_style, isort_config_file=isort_config_file) == 1
	advanced_file_regression.check_file(tmp_pathplus / "code.py")
	check_out(capsys.readouterr(), advanced_data_regression)

	# Calling a second time shouldn't change anything
	assert reformat_file(tmp_pathplus / "code.py", yapf_style=yapf_style, isort_config_file=isort_config_file) == 0
	advanced_file_regression.check_file(tmp_pathplus / "code.py")


@pytest.mark.usefixtures("demo_environment")
def test_reformatter_class(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		capsys,
		yapf_style: str,
		isort_config_file: str,
		):

	isort_config = Config(settings_file=isort_config_file)
	r = Reformatter(tmp_pathplus / "code.py", yapf_style=yapf_style, isort_config=isort_config)

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_string()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.to_file()

	with pytest.raises(ValueError, match=r"'Reformatter.run\(\)' must be called first!"):
		r.get_diff()

	assert r.run() == 1
	r.to_file()

	advanced_file_regression.check_file(tmp_pathplus / "code.py")
	advanced_file_regression.check(r.to_string(), extension="._py_")

	captured = capsys.readouterr()

	assert not captured.out
	assert not captured.err

	# Calling a second time shouldn't change anything
	r = Reformatter(tmp_pathplus / "code.py", yapf_style=yapf_style, isort_config=isort_config)
	assert r.run() == 0
	r.to_file()

	advanced_file_regression.check_file(tmp_pathplus / "code.py")


@pytest.mark.usefixtures("demo_environment")
def test_cli(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		advanced_data_regression: AdvancedDataRegressionFixture,
		yapf_style: str,
		isort_config_file: str,
		):

	result: Result

	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--yapf-style", yapf_style, "--isort-config", isort_config_file],
				)

	assert result.exit_code == 1

	advanced_file_regression.check_file(tmp_pathplus / "code.py")

	check_out(result, advanced_data_regression)

	# Calling a second time shouldn't change anything
	with in_directory(tmp_pathplus):
		runner = CliRunner(mix_stderr=False)
		result = runner.invoke(
				main,
				args=["code.py", "--yapf-style", yapf_style, "--isort-config", isort_config_file],
				)

	assert result.exit_code == 0
