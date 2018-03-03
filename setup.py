import re
import sys
from codecs import open

import setuptools

requires = [
    'requests>=2.18.4',
    'six>=1.11.0'
]

extras_require = {
    ":python_version<'3.2'": ['configparser'],
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
    install_requires=requires,
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
