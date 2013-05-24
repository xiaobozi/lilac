from setuptools import setup
from lilac import version

setup(
    name='lilac',
    version=version,
    author='hit9',
    author_email='nz2324@126.com',
    description='A static blog generator.',
    license='MIT',
    keywords='static blog generator, markdown, toml, posts',
    url='http://github.com/hit9/golb',
    long_description=open('README.md').read(),
    packages=['lilac'],
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'lilac = lilac.cli:main'
        ]
    },
    install_requires = open("requirements.pip").read().splitlines()
)
