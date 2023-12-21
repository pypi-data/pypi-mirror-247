import configparser


class AutProperties:
    properties = {}

    def __init__(self):
        raise Exception("Utility class")

    @classmethod
    def reset_defaults(cls):
        cls.properties.clear()
        cls.set_property(Property.MAGNIFAI_HOST, "http://localhost")
        cls.set_property(Property.MAGNIFAI_AUTH_HOST, "http://localhost")
        cls.set_property(Property.AUTH_PORT, "8080")
        cls.set_property(Property.AUTH_TOKEN_THRESHOLD_SECONDS, "30")
        cls.set_property(Property.DASHBOARDAPI_PORT, "3274")
        cls.set_property(Property.ASSETS_PORT, "2773")
        cls.set_property(Property.METERING_PORT, "6383")
        cls.set_property(Property.MAGNIFAIAPI_PORT, "6246")

    @classmethod
    def load_property_file(cls, property_file_name):
        try:
            config = configparser.ConfigParser()
            config.read(property_file_name)
            cls.set_property(Property.MAGNIFAI_HOST, config['Global']['host'])
            cls.set_property(Property.MAGNIFAI_PORT, config['Global']['port'])
            cls.set_property(Property.MAGNIFAI_AUTH_HOST, config['Auth']['host'])
            cls.set_property(Property.AUTH_PORT, config['Auth']['port'])
            cls.set_property(Property.AUTH_USER, config['Auth']['user'])
            cls.set_property(Property.AUTH_PASSWORD, config['Auth']['password'])
            cls.set_property(Property.AUTH_TOKEN_THRESHOLD_SECONDS, config['Auth']['token.threshold.seconds'])
            cls.set_property(Property.DASHBOARDAPI_PORT, config['dashboard-api']['port'])
            cls.set_property(Property.ASSETS_PORT, config['assets-api']['port'])
            cls.set_property(Property.METERING_PORT, config['metering-api']['port'])
            cls.set_property(Property.MAGNIFAIAPI_PORT, config['magnifai-api']['port'])
        except:
            pass

    @classmethod
    def get_property(cls, key):
        return cls.properties.get(key)

    @classmethod
    def set_property(cls, key, value):
        cls.properties[key] = value

    @classmethod
    def set_common_port(cls, port):
        cls.set_property(Property.MAGNIFAI_PORT.getKey(), str(port))
        cls.properties.pop(Property.AUTH_PORT.getKey(), None)
        cls.properties.pop(Property.DASHBOARDAPI_PORT.getKey(), None)
        cls.properties.pop(Property.ASSETS_PORT.getKey(), None)
        cls.properties.pop(Property.MAGNIFAIAPI_PORT.getKey(), None)


class Property:
    MAGNIFAI_HOST = "magnifai.host"
    MAGNIFAI_AUTH_HOST = "magnifai_auth.host"
    MAGNIFAI_PORT = "magnifai.port"
    AUTH_PORT = "auth.port"
    AUTH_USER = "auth.user"
    AUTH_PASSWORD = "auth.password"
    AUTH_TOKEN_THRESHOLD_SECONDS = "auth.token.threshold.seconds"
    DASHBOARDAPI_PORT = "dashboardapi.port"
    ASSETS_PORT = "assets.port"
    METERING_PORT = "metering.port"
    MAGNIFAIAPI_PORT = "magnifaiapi.port"
