import re

from codecs import open

from setuptools import find_packages, setup

requires = ['requests>=2.13.0']

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
)
