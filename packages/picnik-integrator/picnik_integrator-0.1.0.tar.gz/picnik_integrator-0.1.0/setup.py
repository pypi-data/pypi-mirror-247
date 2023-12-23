# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picnik_integration']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'picnik-integrator',
    'version': '0.1.0',
    'description': 'Numerical integration functions developed to work with the picnik package. Includes: Trapezoid, Simpson and Romberg.',
    'long_description': 'This module defines numerical integration for thermokinetic studies\n',
    'author': 'ErickErock',
    'author_email': 'ramirez.orozco.erick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
