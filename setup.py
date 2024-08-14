from setuptools import setup

setup(
  name='Barzooka',
  version='0.1.1',
  author='Nico Riedel, Vladislav Nachev',
  author_email='vladislav.nachev@charite.de',
  packages=['barzooka'],
  license='LICENSE.txt',
  description='Barzooka is a deep convolutional neural network that screens publication PDFs and checks for bar graphs of continuous data and more informative alternatives to bar graphs, like dot plots, box plots and histograms.',
  long_description=open('README.md').read(),
  install_requires=[
      "fastai==2.7.13",
      "pandas==2.2.2",
      "pytest==8.3.2",
      "importlib_resources==6.4.0",
  ],
)
