# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['priceloop']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3',
 'boto3>=1.34.4,<2.0.0',
 'frozendict>=2.3,<3.0',
 'httpx>=0.15.0,<0.24.0',
 'pandas>=2.0,<3.0',
 'priceloop-api==0.210.5.dev0',
 'python-dateutil>=2.8.0,<3',
 'requests>=2.25,<3.0',
 'tenacity==8.2.3']

setup_kwargs = {
    'name': 'priceloop',
    'version': '0.1.0b0',
    'description': 'python interface to interact with priceloop platform',
    'long_description': 'None',
    'author': 'Priceloop',
    'author_email': 'dev@priceloop.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
