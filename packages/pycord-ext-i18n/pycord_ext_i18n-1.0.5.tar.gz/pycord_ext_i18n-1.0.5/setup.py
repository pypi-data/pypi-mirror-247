import re
from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()



setup(name='pycord_ext_i18n',
      version='1.0.5',
      author='mantouisyummy',
      author_email='opcantel@gmail.com',
      description='A regular localization Library for pycord.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Mantou-9487/pycord_ext_i18n',
      project_urls={
          'Issue Tracker': 'https://github.com/Mantou-9487/pycord_ext_i18n/issues'
      },
      packages=['pycord_ext_i18n'],
      license='GNU',
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Natural Language :: English'
      ],
      python_requires='>=3.10'
)