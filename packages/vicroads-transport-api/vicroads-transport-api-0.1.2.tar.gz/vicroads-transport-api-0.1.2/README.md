# VicRoads Data Exchange Python API Wrapper

This Python package provides an asynchronous API wrapper for accessing transportation updates from the VicRoads Data Exchange platform. The wrapper supports retrieval of various transportation data, including service alerts, trip updates, and vehicle positions for metro trains, buses, and trams.

## Installation

You can install the package using `pip`:

```bash
pip install vicroads-data-exchange-api
```

## Usage
### Initialization

First, import the required modules, create a DataExchangeClient instance, and instantiate the GTFS_R class:

```python
from vicroads_data_exchange_api import DataExchangeClient, GTFS_R
# Create a DataExchangeClient instance
client = DataExchangeClient('your_api_key_here')
# Initialize GTFS_R with the DataExchangeClient instance
gtfs_api = GTFS_R(client)
```


### Retrieving Service Alerts


```python
yarra_service_alerts = await gtfs_api.yarra_trams_service_alerts()
metro_train_alerts = await gtfs_api.metro_trains_service_alerts()
```


### Retrieving Trip Updates

```python
bus_updates = await gtfs_api.metro_bus_trip_updates()
tram_updates = await gtfs_api.yarra_trams_trip_updates()
```

### Retrieving Vehicle Positions


```python
train_positions = await gtfs_api.metro_trains_vehicle_positions()
tram_positions = await gtfs_api.yarra_trams_vehicle_positions()
```


### Documentation

For further details and available methods, refer to the API Documentation.

## Contributing

Feel free to contribute by opening issues or submitting pull requests. We welcome improvements, bug fixes, or additional features.
License

## License

This project is licensed under the MIT License - see the LICENSE file for details.