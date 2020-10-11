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
	  - |travis| |actions_windows| |actions_macos| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|



.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/yapf-isort/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/yapf-isort
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/yapf-isort/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/yapf-isort/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/yapf-isort/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/yapf-isort/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/yapf-isort/requirements/?branch=master
	:alt: Requirements Status

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

.. |license| image:: https://img.shields.io/github/license/domdfcoding/yapf-isort
	:target: https://github.com/domdfcoding/yapf-isort/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/yapf-isort
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/yapf-isort/v0.3.2
	:target: https://github.com/domdfcoding/yapf-isort/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/yapf-isort
	:target: https://github.com/domdfcoding/yapf-isort/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields

|

Installation
--------------

.. start installation

``yapf-isort`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install yapf-isort

.. end installation
