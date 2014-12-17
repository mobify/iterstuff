import os
import os.path
from setuptools import setup

PROJECT = 'iterstuff'
VERSION = '0.0.1'

# The base path is the directory where setup.py lives
BASE = os.path.abspath(os.path.dirname(__file__))
DEPENDENCIES = os.path.join(BASE, 'dependencies.pip')

setup(author='Mobify',
      author_email='product@mobify.com',
      name=PROJECT,
      version=VERSION,

      # Automatically generates a list of all the packages under the
      # project directory.
      packages=[
          os.path.basename(d)
          for d in (os.path.join(BASE, _) for _ in os.listdir(BASE))
          if os.path.isdir(d) and os.path.exists(os.path.join(d, '__init__.py'))
      ],

      # Generates a list of required packages from dependencies.pip
      install_requires=[
          line
          for line in (_.strip() for _ in open(DEPENDENCIES))
          if line and (not line.startswith('#'))
      ],

      zip_safe=True)
