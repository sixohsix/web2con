from setuptools import setup, find_packages
import sys, os

version = '0.1beta'

setup(name='web2con',
      version=version,
      description="Universal Web API connector",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Mike Verdone',
      author_email='mike.verdone@gmail.com',
      url='http://mike.verdone.ca/web2con',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
