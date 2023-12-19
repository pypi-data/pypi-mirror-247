from .client import DataExchangeClient
from google.transit.gtfs_realtime_pb2 import FeedMessage
from google._upb._message import RepeatedCompositeContainer
from .gtfs_model import *


class GTFS_R:
    """
    Request class for GTFS-R data, providing access to various transportation updates.
    """

    API_URL = "opendata/v1/gtfsr"
    YARRA_URL = "opendata/gtfsr/v1"

    def __init__(self, client: DataExchangeClient):
        """
        Initialize GTFS_R with a DataExchangeClient instance.

        Args:
        - client (DataExchangeClient): The client used to make API requests.
        """
        self._client = client

    async def _get(self, path: str, base_url: str = "") -> RepeatedCompositeContainer:
        """
        Retrieves gRPC message from the API endpoint and deserializes it.

        Args:
        - path (str): The API endpoint path to retrieve data from.

        Returns:
        - The deserialized entity from the gRPC message.
        """
        if base_url == "":
            base_url = self.API_URL
        response = await self._client.get(f"{base_url}/{path}")
        feed = FeedMessage()
        feed.ParseFromString(response)
        return feed.entity

    async def _format_service_alert(
        self, response: RepeatedCompositeContainer
    ) -> list[ServiceAlert]:
        """
        Formats a service alert.
        """
        return [
            ServiceAlert.model_validate(service_alert) for service_alert in response
        ]

    async def _format_trip_update(
        self, response: RepeatedCompositeContainer
    ) -> list[TransportUpdate]:
        return [TransportUpdate.model_validate(trip) for trip in response]

    async def yarra_trams_service_alerts(self) -> list[ServiceAlert]:
        """
        Retrieves yarra tram service alerts, primarily cancellations.

        Returns:
        - List of ServiceAlert objects representing train service alerts.
        """
        response = await self._get("tram/servicealert", self.YARRA_URL)
        return await self._format_service_alert(response)

    async def metro_trains_service_alerts(self) -> list[ServiceAlert]:
        """
        Retrieves metro train service alerts, primarily cancellations.

        Returns:
        - List of ServiceAlert objects representing train service alerts.
        """
        response = await self._get("metrotrain-servicealerts")
        return await self._format_service_alert(response)

    async def metro_bus_trip_updates(self) -> list[TransportUpdate]:
        """
        Retrieves metro bus trip updates.

        Returns:
        - List of TransportUpdate objects representing bus trip updates.
        """
        response = await self._get("metrobus-tripupdates")
        return await self._format_trip_update(response)

    async def metro_trains_trip_updates(self) -> list[TransportUpdate]:
        """
        Retrieves metro train trip updates.

        Returns:
        - List of TransportUpdate objects representing train trip updates.
        """
        response = await self._get("metrotrain-tripupdates")
        return await self._format_trip_update(response)

    async def yarra_trams_trip_updates(self) -> list[TransportUpdate]:
        """
        Retrieves yarra tram trip updates.

        Returns:
        - List of TransportUpdate objects representing yarra tram trip updates.
        """
        response = await self._get("tram/tripupdates", self.YARRA_URL)
        return await self._format_trip_update(response)

    async def metro_trains_vehicle_positions(self) -> TrainPositions:
        """
        Retrieves live information of train positions.

        Returns:
        - List of TrainPosition objects representing live train positions.
        """
        response = await self._get("metrotrain-vehicleposition-updates")
        return TrainPositions(
            vehicle_positions=[
                VehiclePosition.model_validate(train) for train in response
            ]
        )

    async def yarra_trams_vehicle_positions(self) -> TramPositions:
        """
        Retrieves live information of tram positions.

        Returns:
        - List of TrainPosition objects representing live tram positions.
        """
        response = await self._get("tram/vehicleposition", self.YARRA_URL)
        return TramPositions(
            vehicle_positions=[
                VehiclePosition.model_validate(tram) for tram in response
            ]
        )
