# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iam_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'iam-sdk-python',
    'version': '0.1.1',
    'description': 'SDK for IAM ',
    'long_description': '# iam-sdk-python',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
