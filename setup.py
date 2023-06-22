from setuptools import setup, find_namespace_packages

setup(name='sorter',
      version='0.1.0',
      description='Very useful code',
      url='http://github.com/dummy_user/useful',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['markdown'],
      entry_points={'console_scripts': ['sort_folder = sorter.sort_02:main']})