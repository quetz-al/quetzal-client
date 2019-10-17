import os

import quetzal.openapi_client.configuration


class Configuration(quetzal.openapi_client.configuration.Configuration,
                    metaclass=quetzal.openapi_client.configuration.TypeWithDefault):
    # Use this later for particular extensions/modifications on the API
    # configuration object

    def __init__(self):
        super().__init__()
        if 'QUETZAL_URL' in os.environ:
            self.host = os.getenv('QUETZAL_URL', '')
        self.username = os.getenv('QUETZAL_USER', '')
        self.password = os.getenv('QUETZAL_PASSWORD', '')
        api_key = os.getenv('QUETZAL_API_KEY', '')
        if api_key:
            self.api_key['X-API-KEY'] = api_key
