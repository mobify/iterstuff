import os
import os.path
from setuptools import setup, find_packages

PROJECT = 'iterstuff'
VERSION = '1.0.3'
PACKAGES = find_packages(exclude=['.vagrant', 'build', 'venv'])

# The base path is the directory where setup.py lives
BASE = os.path.abspath(os.path.dirname(__file__))
DEPENDENCIES = os.path.join(BASE, 'dependencies.pip')

setup(
    author='Mobify',
    author_email='product@mobify.com',
    name=PROJECT,
    version=VERSION,
    packages=PACKAGES,

    description='Useful tools for working with iterators',
    keywords='iterator generator development',
    url='https://github.com/mobify/iterstuff',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],

    install_requires=[],

    zip_safe=True
)
