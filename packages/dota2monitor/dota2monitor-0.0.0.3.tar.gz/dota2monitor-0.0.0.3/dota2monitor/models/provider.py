class Provider:
    def __init__(self, provider_data):
        self.name = provider_data.get('name')
        self.appid = provider_data.get('appid')
        self.version = provider_data.get('version')
        self.timestamp = provider_data.get('timestamp')