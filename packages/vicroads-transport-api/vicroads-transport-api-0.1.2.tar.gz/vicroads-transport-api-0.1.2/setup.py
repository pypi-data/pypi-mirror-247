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
    'version': '0.1.2',
    'description': 'An async Python wrapper for the VicRoads DataExchange API',
    'long_description': "# VicRoads Data Exchange Python API Wrapper\n\nThis Python package provides an asynchronous API wrapper for accessing transportation updates from the VicRoads Data Exchange platform. The wrapper supports retrieval of various transportation data, including service alerts, trip updates, and vehicle positions for metro trains, buses, and trams.\n\n## Installation\n\nYou can install the package using `pip`:\n\n```bash\npip install vicroads-data-exchange-api\n```\n\n## Usage\n### Initialization\n\nFirst, import the required modules, create a DataExchangeClient instance, and instantiate the GTFS_R class:\n\n```python\nfrom vicroads_data_exchange_api import DataExchangeClient, GTFS_R\n# Create a DataExchangeClient instance\nclient = DataExchangeClient('your_api_key_here')\n# Initialize GTFS_R with the DataExchangeClient instance\ngtfs_api = GTFS_R(client)\n```\n\n\n### Retrieving Service Alerts\n\n\n```python\nyarra_service_alerts = await gtfs_api.yarra_trams_service_alerts()\nmetro_train_alerts = await gtfs_api.metro_trains_service_alerts()\n```\n\n\n### Retrieving Trip Updates\n\n```python\nbus_updates = await gtfs_api.metro_bus_trip_updates()\ntram_updates = await gtfs_api.yarra_trams_trip_updates()\n```\n\n### Retrieving Vehicle Positions\n\n\n```python\ntrain_positions = await gtfs_api.metro_trains_vehicle_positions()\ntram_positions = await gtfs_api.yarra_trams_vehicle_positions()\n```\n\n\n### Documentation\n\nFor further details and available methods, refer to the API Documentation.\n\n## Contributing\n\nFeel free to contribute by opening issues or submitting pull requests. We welcome improvements, bug fixes, or additional features.\nLicense\n\n## License\n\nThis project is licensed under the MIT License - see the LICENSE file for details.",
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
