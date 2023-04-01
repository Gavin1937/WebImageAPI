from setuptools import setup


# get descriptions
description = 'A Python3 API to fetch info and download images from popular websites.'
long_description = ''
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

# load __version__.py
version = {}
with open('./WebImageAPI/__version__.py', 'r', encoding='utf-8') as file:
    exec(file.read(), version)

# load requirements.txt
requirements = []
with open('./requirements.txt', 'r', encoding='utf-8') as file:
    requirements = [line.strip() for line in file.readlines() if len(line.strip()) > 0]


# package settings
setup(
    name='WebImageAPI',
    author='Gavin1937',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Gavin1937/WebImageAPI',
    version=version['__version__'],
    packages=[
        'WebImageAPI',
        'WebImageAPI.Agents',
        'WebImageAPI.Types',
        'WebImageAPI.Utils'
    ],
    python_requires='>=3.8.0',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

