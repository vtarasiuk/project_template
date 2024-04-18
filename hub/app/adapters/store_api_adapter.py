import json
import logging
from typing import List

import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        url = f"{self.api_base_url}/processed_agent_data/"

        data = [processed_agent_data.model_dump_json() for processed_agent_data in processed_agent_data_batch]
        response = requests.post(url, data='[' + ','.join(data) + ']', headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            logging.info(f"Invalid Hub response\nData: {data}\nResponse: {response}")
            return False
        return True
