from setuptools import setup

setup(
  name='Barzooka',
  version='0.1.0',
  author='Nico Riedel',
  author_email='nico.riedel@bih-charite.de',
  packages=['barzooka'],
  license='LICENSE.txt',
  description='Barzooka is a deep convolutional neural network that screens publication PDFs and checks for bar graphs of continuous data and more informative alternatives to bar graphs, like dot plots, box plots and histograms.',
  long_description=open('README.md').read(),
  install_requires=[
      "fastai >= 2.0",
      "numpy",
      "pandas",
      "pytest",
  ],
)