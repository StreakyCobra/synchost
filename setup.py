import synchost as sn
from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name=sn.__appname__,
      version=sn.__version__,
      description=sn.__description__,
      long_description=long_description,
      author=sn.__author__,
      author_email=sn.__authormail__,
      url=sn.__projecturl__,
      packages=['synchost'],
      scripts=['scripts/synch'],
      install_requires=['termcolor'])
