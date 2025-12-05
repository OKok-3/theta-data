from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient

from thetadata.options.list import OptionsList


class Options:
    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client

        self.list = OptionsList(self.client)
