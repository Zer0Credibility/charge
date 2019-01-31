from setuptools import setup
# from rebuild_tools import version

setup(name='charge',
      version='a0.5_dev3',
      description='Module for analysis of potentiostatic data',
      author='Clayton M. Rabideau',
      author_email='cmr57@cam.ac.uk',
      packages=['charge'],
      install_requires=['numpy', 'num2words', 'pandas', 'tqdm', 'scipy', 'statsmodels', 'matplotlib']
      )
