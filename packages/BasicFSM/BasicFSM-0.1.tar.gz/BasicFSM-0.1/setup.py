from distutils.core import setup
setup(
  name = 'BasicFSM',         # How you named your package folder (MyLib)
  packages = ['BasicFSM'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A lightweight library to manage a Finite State Machine',   # Give a short description about your library
  author = 'Levorin',                   # Type in your name
  author_email = 'frankigeno@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Frankigeno/BasicFSM',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Frankigeno/BasicFSM/archive/refs/tags/v0.1.0.tar.gz',    # I explain this later on
  keywords = ['FSM', 'Async'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10'
  ],
)