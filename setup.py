from setuptools import setup
import ggs

setup(name='ggs',
      description='Greedy grid search for hyper-parameter optimization.',
      url='https://github.com/enzobusseti/greedy_grid_search',
      author_email='enzo.busseti@gmail.com',
      author='Enzo Busseti',
      license='GPLv3',
      version=ggs.__version__,
      tests_require=["nose"],
      py_modules=["ggs"]
      )
