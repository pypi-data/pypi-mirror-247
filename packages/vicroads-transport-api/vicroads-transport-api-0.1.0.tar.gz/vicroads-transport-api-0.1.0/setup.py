# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vicroads_transport_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.1,<4.0.0',
 'gtfs-realtime-bindings>=1.0.0,<2.0.0',
 'protobuf>=4.25.1,<5.0.0',
 'pydantic>=2.5.2,<3.0.0']

setup_kwargs = {
    'name': 'vicroads-transport-api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'saikumarmk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
