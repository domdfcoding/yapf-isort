###########
yapf-isort
###########

.. start short_desc

**yapf 💌 isort**

.. end short_desc

Script and `pre-commit hook <https://pre-commit.com/>`_
to run `yapf <https://github.com/google/yapf>`_
and `isort <https://pycqa.github.io/isort/>`_
together for formatting Python source files.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/yapf-isort/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/yapf-isort/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/yapf-isort/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/yapf-isort/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/yapf-isort/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/yapf-isort/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/domdfcoding/yapf-isort/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/yapf-isort/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/yapf-isort?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/yapf-isort?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/yapf-isort
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/yapf-isort
	:target: https://pypi.org/project/yapf-isort/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/yapf-isort?logo=python&logoColor=white
	:target: https://pypi.org/project/yapf-isort/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/yapf-isort
	:target: https://pypi.org/project/yapf-isort/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/yapf-isort
	:target: https://pypi.org/project/yapf-isort/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/yapf-isort?logo=anaconda
	:target: https://anaconda.org/domdfcoding/yapf-isort
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/yapf-isort?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/yapf-isort
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/yapf-isort
	:target: https://github.com/domdfcoding/yapf-isort/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/yapf-isort
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/yapf-isort/v0.6.0
	:target: https://github.com/domdfcoding/yapf-isort/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/yapf-isort
	:target: https://github.com/domdfcoding/yapf-isort/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/yapf-isort
	:target: https://pypi.org/project/yapf-isort/
	:alt: PyPI - Downloads

.. end shields

|

Installation
--------------

.. start installation

``yapf-isort`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install yapf-isort

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install yapf-isort

.. end installation
