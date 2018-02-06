import re
from codecs import open

from setuptools import find_packages, setup

requires = ['requests>=2.18.4', 'six>=1.11.0']

with open('twitch/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='python-twitch-client',
    version=version,
    description='Easy to use Python library for accessing the Twitch API',
    author='Tomaz Sifrer',
    author_email='tomazz.sifrer@gmail.com',
    url='https://github.com/tsifrer/python-twitch-client',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ]
)
