# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sqlyte']
install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'sqlyte',
    'version': '0.1.2',
    'description': 'a simple SQLite interface',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
