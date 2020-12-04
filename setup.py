import re
import sys
from codecs import open

import setuptools
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args.split(" "))
        sys.exit(errno)


cmdclass = {"test": PyTest}

if "build_docs" in sys.argv:
    from sphinx.setup_command import BuildDoc

    cmdclass["build_docs"] = BuildDoc

requires = ["requests>=2.23.0"]

test_requirements = [
    "black==20.8b1",
    "codecov>=2.1.10",
    "flake8-isort>=4.0.0",
    "flake8>=3.8.4",
    "isort>=5.6.4",
    "pytest-cov>=2.10.1",
    "pytest>=6.1.2",
    "responses>=0.12.1",
]

doc_reqs = ["Sphinx==3.3.1", "sphinx_rtd_theme==0.5.0"]

extras_require = {
    "doc": doc_reqs,
    "test": test_requirements,
}

if int(setuptools.__version__.split(".")[0]) < 18:
    extras_require = {}
    if sys.version_info < (3, 2):
        requires.append("configparser")


with open("twitch/__init__.py", "r") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setuptools.setup(
    name="python-twitch-client",
    version=version,
    description="Easy to use Python library for accessing the Twitch API",
    author="Tomaz Sifrer",
    author_email="tomazz.sifrer@gmail.com",
    url="https://github.com/tsifrer/python-twitch-client",
    packages=setuptools.find_packages(include=["twitch", "twitch.*"]),
    cmdclass=cmdclass,
    install_requires=requires,
    tests_require=test_requirements,
    extras_require=extras_require,
    python_requires=">=3.6, <4",
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
