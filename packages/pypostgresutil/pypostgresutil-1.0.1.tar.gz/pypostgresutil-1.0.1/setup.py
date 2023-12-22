from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(
  name='pypostgresutil',
  version='1.0.1',
  author='An0nX',
  author_email='example@gmail.com',
  description='Python library for simple PostgreSQL management',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/An0nX/PostgreSQLController',
  packages=find_packages(),
  install_requires=['psycopg2', 'loguru'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='Python Library PostgreSQL Management Pypi Tool Database Interaction Relational Databases Python Programming ',
  python_requires='>=3.7'
)
