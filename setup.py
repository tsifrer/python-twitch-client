import re
import sys
from codecs import open

import setuptools
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    """Handle test execution from setup."""

    user_options = [('pytest-args=', 'a', "Arguments to pass into pytest")]

    def initialize_options(self):
        print("here")
        """Initialize the PyTest options."""
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def finalize_options(self):
        """Finalize the PyTest options."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run the PyTest testing suite."""
        try:
            import pytest
        except ImportError:
            raise ImportError('Running tests requires additional dependencies.'
                              '\nPlease run (pip install python-twitch-client[test])')

        errno = pytest.main(self.pytest_args.split(" "))
        sys.exit(errno)


cmdclass = {'test': PyTest}  # Define custom commands.


if "build_docs" in sys.argv:
    try:
        from sphinx.setup_command import BuildDoc
    except ImportError:
        raise ImportError(
            'Running the documenation builds has additional'
            ' dependencies. Please run (pip install python-twitch-client[doc])'
        )
    cmdclass["build_docs"] = BuildDoc

requires = [
    'requests>=2.18.4',
    'six>=1.11.0'
]

test_reqs = [
    'codecov==2.0.15',
    'configparser==3.5.0',
    'flake8-import-order==0.17.1',
    'flake8==3.5.0',
    'pycodestyle==2.3.1',
    'pytest-cov==2.5.1',
    'pytest==3.5.1',
    'responses==0.9.0'
]

doc_reqs = [
    'Sphinx==1.7.4',
    'sphinx-autobuild==0.7.1',
    'sphinx_rtd_theme==0.3.1'
]

extras_require = {
    ":python_version<'3.2'": ['configparser'],
    "doc": doc_reqs,
    "test": test_reqs
}

if int(setuptools.__version__.split('.')[0]) < 18:
    extras_require = {}
    if sys.version_info < (3, 2):
        requires.append('configparser')


with open('twitch/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setuptools.setup(
    name='python-twitch-client',
    version=version,
    description='Easy to use Python library for accessing the Twitch API',
    author='Tomaz Sifrer',
    author_email='tomazz.sifrer@gmail.com',
    url='https://github.com/tsifrer/python-twitch-client',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    cmdclass=cmdclass,
    install_requires=requires,
    tests_require=test_reqs,
    extras_require=extras_require,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
