import os

import quetzal.openapi_client.configuration


class Configuration(quetzal.openapi_client.configuration.Configuration):
    # Use this later for particular extensions/modifications on the API
    # configuration object

    def __init__(self):
        super().__init__()
        if 'QUETZAL_URL' in os.environ:
            self.host = os.getenv('QUETZAL_URL', '')
        self.username = os.getenv('QUETZAL_USER', '')
        self.password = os.getenv('QUETZAL_PASSWORD', '')

