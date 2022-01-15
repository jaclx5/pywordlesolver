from distutils.core import setup

setup(name='pywordlesolver',
      version='1.0',
      description='Python WORDLE game and solver.',
      author='JACLX5',
      author_email='cincominutosdatascience@gmail.com',
      packages=['pywordlesolver'],
      scripts=['pywordlesolver/wordle.py'],

      package_data={"pywordlesolver": ["data/*.txt"]}
      )

